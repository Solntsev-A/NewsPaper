from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import send_post_notification

@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, action, **kwargs):
    if action != 'post_add':
        return

    post = instance.postInclude
    category = instance.categoryInclude

    emails = User.objects.filter(
        subscriptions__category=category
    ).values_list('email', flat=True)

    send_post_notification.delay(
        list(emails),
        category.name,
        post.title,
        post.text,
        post.get_absolute_url()
    )

# Вариант до использования celery и redis
# @receiver(m2m_changed, sender=PostCategory)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новый пост в любимой категории  {instance.category}'
#
#     text_content = (
#         f'Пост: {instance.title}\n'
#         f'Содержание : {instance.text}\n\n'
#         f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Пост: {instance.title}<br>'
#         f'Содержание: {instance.text}<br><br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на пост</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()