from allauth.socialaccount.providers.mediawiki.provider import settings
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.db.models.signals import post_delete
from django.template.loader import render_to_string
from django.conf import settings

from .models import Posts, PostCategory

def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/post/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email= settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)








# @receiver(post_delete, sender=Posts)
# def notify_managers_appointment_canceled(sender, instance, **kwargs):
#     subject = f'{instance.client_name} has canceled his appointment!'
#     mail_managers(
#         subject=subject,
#         message=f'Canceled appointment for {instance.date.strftime("%d %m %Y")}',
#     )
#
#     print(subject)