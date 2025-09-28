from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import User, JobAdvert, JobApplication, Skill, Category
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    JobAdvertSerializer, JobAdvertCreateSerializer, JobApplicationSerializer,
    JobApplicationCreateSerializer, SkillSerializer, CategorySerializer
)
from .tasks import send_application_notification_email, send_welcome_email
from .permissions import IsOwnerOrReadOnly


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Send welcome email asynchronously
        send_welcome_email.delay(user.id)


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class JobAdvertListView(generics.ListAPIView):
    serializer_class = JobAdvertSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_type', 'experience_level', 'is_remote', 'is_active']
    search_fields = ['title', 'description', 'requirements', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = JobAdvert.objects.filter(is_active=True).prefetch_related('skills__skill', 'categories__category')
        
        # Filter by skills
        skills = self.request.query_params.getlist('skills')
        if skills:
            queryset = queryset.filter(skills__skill_id__in=skills).distinct()
        
        # Filter by categories
        categories = self.request.query_params.getlist('categories')
        if categories:
            queryset = queryset.filter(categories__category_id__in=categories).distinct()
        
        # Filter by salary range
        min_salary = self.request.query_params.get('min_salary')
        max_salary = self.request.query_params.get('max_salary')
        if min_salary:
            queryset = queryset.filter(salary_min__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary_max__lte=max_salary)
        
        # Filter by deadline
        deadline = self.request.query_params.get('deadline')
        if deadline:
            queryset = queryset.filter(application_deadline__gte=timezone.now().date())
        
        return queryset


class JobAdvertDetailView(generics.RetrieveAPIView):
    serializer_class = JobAdvertSerializer
    permission_classes = [permissions.AllowAny]
    queryset = JobAdvert.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class JobAdvertCreateView(generics.CreateAPIView):
    serializer_class = JobAdvertCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


class JobAdvertUpdateView(generics.UpdateAPIView):
    serializer_class = JobAdvertCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = JobAdvert.objects.all()

    def get_queryset(self):
        return JobAdvert.objects.filter(employer=self.request.user)


class JobAdvertDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = JobAdvert.objects.all()

    def get_queryset(self):
        return JobAdvert.objects.filter(employer=self.request.user)



class JobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['applied_at', 'updated_at']
    ordering = ['-applied_at']

   
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return JobApplication.objects.none()
        if not self.request.user.is_authenticated:
            return JobApplication.objects.none()
        return JobApplication.objects.filter(user_type=self.request.user.user_type)



class JobApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'employer':
            return JobApplication.objects.filter(job_advert__employer=user)
        else:
            return JobApplication.objects.filter(job_seeker=user)


class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        job_advert_id = kwargs.get('job_advert_id')
        job_advert = get_object_or_404(JobAdvert, id=job_advert_id, is_active=True)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Add context for the serializer
        serializer.context['job_advert_id'] = job_advert_id
        serializer.context['request'] = request
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Send notification email asynchronously
        send_application_notification_email.delay(serializer.instance.id)
        
        return Response(
            JobApplicationSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class JobApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'employer':
            return JobApplication.objects.filter(job_advert__employer=user)
        else:
            return JobApplication.objects.filter(job_seeker=user)


class SkillListView(generics.ListAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Skill.objects.all()


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request):
    return Response({
        'message': 'ALX Project Nexus API',
        'endpoints': {
            'auth': {
                'register': '/auth/register/',
                'login': '/auth/login/',
                'profile': '/auth/profile/',
            },
            'job_adverts': {
                'list': '/api/adverts/',
                'detail': '/api/adverts/{id}/',
                'create': '/api/adverts/create/',
                'update': '/api/adverts/{id}/update/',
                'delete': '/api/adverts/{id}/delete/',
            },
            'applications': {
                'list': '/api/applications/',
                'detail': '/api/applications/{id}/',
                'create': '/api/adverts/{id}/apply/',
                'update': '/api/applications/{id}/update/',
            },
            'skills': '/api/skills/',
            'categories': '/api/categories/',
            'docs': '/api/docs/',
            'schema': '/api/schema/',
        }
    })
