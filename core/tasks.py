from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import JobApplication, JobAdvert


@shared_task
def send_application_notification_email(application_id):
    """
    Send email notification to employer when a new job application is submitted
    """
    try:
        application = JobApplication.objects.select_related(
            'job_advert', 'job_advert__employer', 'job_seeker'
        ).get(id=application_id)
        
        employer = application.job_advert.employer
        job_seeker = application.job_seeker
        job_advert = application.job_advert
        
        subject = f"New Application for {job_advert.title}"
        
        html_message = render_to_string('emails/new_application.html', {
            'employer': employer,
            'job_seeker': job_seeker,
            'job_advert': job_advert,
            'application': application,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employer.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Notification sent to {employer.email}"
        
    except JobApplication.DoesNotExist:
        return "Application not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@shared_task
def send_application_status_email(application_id, old_status, new_status):
    """
    Send email notification to job seeker when application status changes
    """
    try:
        application = JobApplication.objects.select_related(
            'job_advert', 'job_seeker'
        ).get(id=application_id)
        
        job_seeker = application.job_seeker
        job_advert = application.job_advert
        
        subject = f"Application Status Update: {job_advert.title}"
        
        html_message = render_to_string('emails/application_status_update.html', {
            'job_seeker': job_seeker,
            'job_advert': job_advert,
            'application': application,
            'old_status': old_status,
            'new_status': new_status,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[job_seeker.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Status update sent to {job_seeker.email}"
        
    except JobApplication.DoesNotExist:
        return "Application not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@shared_task
def send_welcome_email(user_id):
    """
    Send welcome email to new users
    """
    try:
        from .models import User
        user = User.objects.get(id=user_id)
        
        subject = "Welcome to ALX Project Nexus Job Board"
        
        html_message = render_to_string('emails/welcome.html', {
            'user': user,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Welcome email sent to {user.email}"
        
    except User.DoesNotExist:
        return "User not found"
    except Exception as e:
        return f"Error sending welcome email: {str(e)}"


@shared_task
def check_expired_job_adverts():
    """
    Check for job adverts that have passed their application deadline
    and mark them as inactive
    """
    from django.utils import timezone
    expired_count = JobAdvert.objects.filter(
        is_active=True,
        application_deadline__lt=timezone.now().date()
    ).update(is_active=False)
    
    return f"Marked {expired_count} job adverts as expired"
