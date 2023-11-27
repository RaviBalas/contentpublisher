from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from common.user_exceptions import GenericException
from common.db_log_handler import log_error
from django_core.settings.base import DEFAULT_FROM_EMAIL


# Error-Code: 2000

def send_email_with_template(request, email_config, email_data):
    try:
        html_content = render_to_string(email_config['template_name'], email_config['context'], request=request)
        email_message = EmailMultiAlternatives(subject=email_data['subject'], body=html_content,
                                               from_email=DEFAULT_FROM_EMAIL, to=email_data['recipient'])

        email_message.attach_alternative(html_content, email_config['content_type'])

        email_message.send(fail_silently=False)
    except SMTPException as e:
        log_error(e, 2500)
        raise GenericException(detail='There was an error sending an email', code=200)
