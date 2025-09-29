from celery import shared_task  # type: ignore
from django.core.mail import send_mail  # type: ignore
from django.conf import settings  # type: ignore
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags  # type: ignore
from .models import JobApplication, JobAdvert  # type: ignore


from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore
from django.utils import timezone

@shared_task
def send_welcome_email(user_id):
    from .models import User  # type: ignore
    user = User.objects.get(id=user_id)
    subject = 'Welcome to ALX Project Nexus'

    # Get the domain from ALLOWED_HOSTS or use localhost
    domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != 'localhost' else 'localhost:8000'
    protocol = 'https' if not settings.DEBUG else 'http'

    context = {
        'user': user,
        'domain': domain,
        'protocol': protocol,
    }

    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

@shared_task
def send_application_notification_email(application_id):
    application = JobApplication.objects.get(id=application_id)
    subject = f'New Application for {application.job_advert.title}'

    # Get the domain from ALLOWED_HOSTS or use localhost
    domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != 'localhost' else 'localhost:8000'
    protocol = 'https' if not settings.DEBUG else 'http'

    context = {
        'application': application,
        'employer': application.job_advert.employer,
        'job_advert': application.job_advert,
        'job_seeker': application.job_seeker,
        'domain': domain,
        'protocol': protocol,
    }

    html_message = render_to_string('emails/new_application.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = application.job_advert.employer.email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

@receiver(post_save, sender=JobApplication)
def update_job_advert_counts(sender, instance, **kwargs):
    """
    Signal handler to update job advert counts automatically
    after a new application is submitted or status changes
    """
    if isinstance(instance, JobApplication):
        job_advert = instance.job_advert
        
        # Recalculate the total applications count for this job advert
        job_advert.applications_count = job_advert.applications.filter(
            status__in=['pending', 'reviewed', 'interview', 'accepted']
        ).count()
        job_advert.save()
        
        # Optionally, update other fields based on the application status change
        # For example, if the application is accepted, update the company's metrics
        
        if hasattr(instance, 'status') and instance.status == 'accepted':
            # Update the employer's metrics or notification
            pass

@receiver(post_save, sender=JobAdvert)
def set_default_application_deadline(sender, instance, created, **kwargs):
    """
    Signal handler to set default application deadline if not provided
    when a new job advert is created
    """
    if created and not instance.application_deadline:
        from datetime import timedelta  # type: ignore
        instance.application_deadline = timezone.now().date() + timedelta(days=30)
        instance.save()
