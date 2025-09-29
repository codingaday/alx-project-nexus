from rest_framework import serializers  # type: ignore
from django.contrib.auth import authenticate  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from .models import User, JobAdvert, JobApplication, Skill, Category, JobAdvertSkill, JobAdvertCategory  # type: ignore


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm',
                 'user_type', 'company_name', 'phone_number', 'bio',
                 'website', 'location')

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError(_("Passwords do not match."))
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError(_("Invalid credentials."))
            if not user.is_active:
                raise serializers.ValidationError(_("User account is disabled."))
            data['user'] = user
        else:
            raise serializers.ValidationError(_("Must include username and password."))
        
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type', 'company_name', 
                 'phone_number', 'bio', 'website', 'location', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class JobAdvertSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), source='skill', write_only=True
    )
    
    class Meta:
        model = JobAdvertSkill
        fields = ('id', 'skill', 'skill_id', 'importance_level')


class JobAdvertCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    
    class Meta:
        model = JobAdvertCategory
        fields = ('id', 'category', 'category_id')


class JobAdvertSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    skills = JobAdvertSkillSerializer(many=True, read_only=True)
    categories = JobAdvertCategorySerializer(many=True, read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = JobAdvert
        fields = ('id', 'employer', 'title', 'description', 'requirements', 
                 'location', 'job_type', 'experience_level', 'salary_min', 
                 'salary_max', 'salary_currency', 'is_remote', 
                 'application_deadline', 'is_active', 'views_count', 
                 'applications_count', 'skills', 'categories', 'created_at', 
                 'updated_at')
        read_only_fields = ('id', 'employer', 'created_at', 'updated_at', 
                           'views_count', 'applications_count')


class JobAdvertCreateSerializer(serializers.ModelSerializer):
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    category_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    
    class Meta:
        model = JobAdvert
        fields = ('title', 'description', 'requirements', 'location', 
                 'job_type', 'experience_level', 'salary_min', 'salary_max', 
                 'salary_currency', 'is_remote', 'application_deadline', 
                 'is_active', 'skill_ids', 'category_ids')
    
    def create(self, validated_data):
        skill_ids = validated_data.pop('skill_ids', [])
        category_ids = validated_data.pop('category_ids', [])
        
        job_advert = JobAdvert.objects.create(
            employer=self.context['request'].user,
            **validated_data
        )
        
        # Add skills
        JobAdvertSkill.objects.bulk_create([
            JobAdvertSkill(job_advert=job_advert, skill_id=skill_id, importance_level=3)
            for skill_id in skill_ids
        ])
        
        # Add categories
        JobAdvertCategory.objects.bulk_create([
            JobAdvertCategory(job_advert=job_advert, category_id=category_id)
            for category_id in category_ids
        ])
        
        return job_advert
    
    def update(self, instance, validated_data):
        skill_ids = validated_data.pop('skill_ids', None)
        category_ids = validated_data.pop('category_ids', None)
        
        # Update job advert fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update skills if provided
        if skill_ids is not None:
            instance.skills.all().delete()
            JobAdvertSkill.objects.bulk_create([
                JobAdvertSkill(job_advert=instance, skill_id=skill_id, importance_level=3)
                for skill_id in skill_ids
            ])
        
        # Update categories if provided
        if category_ids is not None:
            instance.categories.all().delete()
            JobAdvertCategory.objects.bulk_create([
                JobAdvertCategory(job_advert=instance, category_id=category_id)
                for category_id in category_ids
            ])
        
        return instance


class JobApplicationSerializer(serializers.ModelSerializer):
    job_seeker = UserSerializer(read_only=True)
    job_advert = JobAdvertSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = ('id', 'job_seeker', 'job_advert', 'cover_letter', 'resume', 
                 'status', 'applied_at', 'updated_at')
        read_only_fields = ('id', 'job_seeker', 'job_advert', 'applied_at', 
                           'updated_at')


from django.core.validators import FileExtensionValidator  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from django.conf import settings  # type: ignore

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(validators=[
        FileExtensionValidator(allowed_extensions=settings.ALLOWED_FILE_EXTENSIONS, message="Invalid file type"),
    ])
    
    class Meta:
        model = JobApplication
        fields = ('cover_letter', 'resume')
    
    def validate(self, data):
        job_seeker = self.context['request'].user
        if job_seeker.user_type != 'job_seeker':
            raise serializers.ValidationError(
                _("Only job seekers can apply for jobs.")
            )
        return data

    def create(self, validated_data):
        job_advert_id = self.context['job_advert_id']
        job_seeker = self.context['request'].user
        
        # Check if already applied
        if JobApplication.objects.filter(
            job_seeker=job_seeker, job_advert_id=job_advert_id
        ).exists():
            raise serializers.ValidationError(
                _("You have already applied for this job.")
            )
        
        return JobApplication.objects.create(
            job_seeker=job_seeker,
            job_advert_id= job_advert_id,
            **validated_data
        )

class EmptySerializer(serializers.Serializer):
    pass
