#Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_user_email(subject, confirm_link, template, user):
    body = render_to_string(template,{'confirm_link': confirm_link, 'user':user})
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(body, 'text/html')
    send_email.send()

BLOOD_TYPE = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)