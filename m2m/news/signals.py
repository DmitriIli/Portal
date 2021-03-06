from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, User, Subscribers
from django.db.models.signals import post_save
from django.core.mail import send_mail, EmailMultiAlternatives
from m2m.celery import app

#запуск процесса по сигналу
# @receiver(post_save, sender=Post)
# def subscribers_notify(sender, instance, created, **kwarg):
#     recipient_list = []
#     postcategory = [i for i in Post.objects.get(pk=instance.id).post_category.all()]
#
#     for item in postcategory:
#         sub = Subscribers.objects.filter(category_id=item).all()
#         if sub:
#             for i in sub:
#                 recipient_list.append(User.objects.get(pk=i.user_id).email)
#     email_list = list(set(recipient_list))
#     if created:
#         html_content = render_to_string(
#             'news/subscriber_notify.html',
#             {
#                 'instance': instance,
#             }
#         )
#         # send_mail(
#         #     subject=f'{instance.title}',
#         #     message=f'{instance.text[:20]}',
#         #     from_email='softb0x@yandex.ru',
#         #     recipient_list=email_list,
#         # )
#         msg = EmailMultiAlternatives(
#             subject=f'{instance.title} {instance.date.strftime("%Y-%M-%d")}',
#             body=f'{instance.text[:20]}  http://127.0.0.1:8000/news/{instance.id}',
#             from_email='softb0x@yandex.ru',
#             to=email_list,
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#
#         msg.send()  # отсылаем
#
#         return redirect('/')


# @receiver(post_save, sender=User)
# def adduser_message(sender, instance, created, **kwarg):
#     if created:
#         html_content = render_to_string(
#             'news/add_new_user.html',
#             {
#                 'instance': instance,
#             }
#         )
#
#         msg = EmailMultiAlternatives(
#             subject=f'Приветсвую тебя {instance.name}',
#             body=f'Приветсвенное письмо для нового пользователя {instance.name}',
#             from_email='softb0x@yandex.ru',
#             to=instance.email,
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#
#         msg.send()  # отсылаем
#
#         return redirect('/')


@app.task()
def add_news_notify(post_pk):
    post = Post.objects.get(pk=post_pk)
    category_list = [i for i in Post.objects.get(pk=post_pk).post_category.all()]
    recipient_list = []
    for item in category_list:
        sub = Subscribers.objects.filter(category_id=item).all()
        if sub:
            for i in sub:
                recipient_list.append(User.objects.get(pk=i.user_id).email)
    email_list = list(set(recipient_list))
    send_mail(
        subject=f'{post.title}',
        message=f'{post.text[:20]}',
        from_email='softb0x@yandex.ru',
        recipient_list=email_list,
    )


def send_notify_add_post(sender, instance, signal, created, *args, **kwargs):
    if created:
        add_news_notify.delay(instance.pk)


post_save.connect(send_notify_add_post, sender=Post)
