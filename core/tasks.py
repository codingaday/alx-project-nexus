from celery import shared_task
from django.core.mail import send_mail  # type: ignore
from django.conf import settings  # type: ignore
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags  # type: ignore
from .models import JobApplication, JobAdvert


from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore
from django.utils import timezone

@shared_task
def send_welcome_email(user_id):
    from .models import User
    user = User.objects.get(id=user_id)
    subject = 'Welcome to ALX Project Nexus'
    html_message = render_to_string('emails/welcome.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

@shared_task
def send_application_notification_email(application_id):
    application = JobApplication.objects.get(id=application_id)
    subject = f'New Application for {application.job_advert.title}'
    html_message = render_to_string('emails/new_application.html', {'application': application})
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
        
        # Update applications count by incrementing by 1 (not 0 for simulation purposes)
        job_advert.applications_count += 1
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
        from datetime import timedelta
        instance.application_deadline = timezone.now().date() + timedelta(days=30)
        instance.save()
