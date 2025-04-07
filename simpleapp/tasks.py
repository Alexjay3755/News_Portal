from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
from simpleapp.models import Post, Category
from celery import shared_task


@shared_task
def create_news_task(pk):
    post = Post.objects.get(id=pk)
    categories = post.category.all()


    for cat in categories:
        subscribers = cat.subscribers.all()
        if subscribers.exists():
            for subscriber in subscribers:

                html_content = render_to_string(
                    'post_created_email.html',
                    {
                        'text': post.preview(),
                        'link': f'{settings.SITE_URL}/post/{pk}'
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=post.title,
                    body='',
                    from_email= settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()




@shared_task
def my_job():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html' )
    msg.send()


