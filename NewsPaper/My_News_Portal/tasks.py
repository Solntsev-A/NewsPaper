from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from .models import Post, Category


@shared_task
def send_post_notification(emails, category_name, title, text, url):
    subject = f'Новый пост в любимой категории {category_name}'
    text_content = (
        f'Пост: {title}\n'
        f'Содержание: {text}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{url}'
    )
    html_content = (
        f'Пост: {title}<br>'
        f'Содержание: {text}<br><br>'
        f'<a href="http://127.0.0.1:8000{url}">Ссылка на пост</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    return f"Sent to {len(emails)} subscribers."

@shared_task
def send_weekly_newsletter():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)

    if not posts.exists():
        return "No new posts this week."

    for category in Category.objects.all():
        category_posts = posts.filter(postCategory=category)
        if not category_posts.exists():
            continue

        subscribers = User.objects.filter(subscriptions__category=category)
        emails = [u.email for u in subscribers if u.email]

        if not emails:
            continue

        subject = f'Новые посты в категории "{category.name}" за неделю'
        text_content = "Ваши новые посты:\n"
        html_content = "<h3>Новые посты за неделю:</h3>"

        for post in category_posts:
            link = f"http://127.0.0.1:8000{post.get_absolute_url()}"
            text_content += f"- {post.title}: {link}\n"
            html_content += f'<p><a href="{link}">{post.title}</a></p>'

        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    return "Weekly newsletter sent successfully."