from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up
from django.conf import settings

# Далее используйте settings.DEFAULT_FROM_EMAIL и settings.SITE_URL по мере необходимости


from .models import PostCategory, Post


def send_notifications(preview, pk, post_name, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/posts/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=post_name,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=Post.categories.through)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        print('Сигнал сработал')
        categories = instance.categories.all()
        subscribers = []
        for post_category in categories:
            subscribers += post_category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)


@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    subject = 'Well come!'
    message = render_to_string('welcome_email.html', {
        'user': user,
    })
    user.email_user(subject, message)