# users/services.py (or wherever send_invitation_email lives)
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from urllib.parse import urlencode

def send_invitation_email(invitation, frontend_url=None):
    """
    Send invitation email to the invited user.
    Accept optional frontend_url to override settings.FRONTEND_URL.
    Returns (success_bool, invitation_url)
    """
    subject = f'Invitation to join {getattr(settings, "SITE_NAME", "Student Tracking Platform")}'

    # Use override if provided, otherwise settings.FRONTEND_URL
    frontend_url = frontend_url or getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')
    # Keep the token as the primary identifier in the link
    invitation_url = f"{frontend_url.rstrip('/')}/accept-invitation?token={invitation.token}"

    context = {
        'invitation': invitation,
        'invitation_url': invitation_url,
        'invited_by': invitation.invited_by.get_full_name() or invitation.invited_by.username,
        'role': invitation.get_role_display(),
    }

    html_message = render_to_string('emails/invitation.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER),
            recipient_list=[invitation.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True, invitation_url
    except Exception as e:
        print(f"Error sending invitation email: {e}")
        return False, invitation_url
