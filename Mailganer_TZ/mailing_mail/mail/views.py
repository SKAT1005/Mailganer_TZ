# coding=utf-8

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from form import MailingForm
from models import User, Mail
from  celery import shared_task
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
app = Celery('main')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.conf.beat_schedule = {
    'Send_mail_to_Client': {
        'task': 'sendmail.tasks.send_mail_task',
        'schedule': 30.0,
    }
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app = Celery('tasks', broker='pyamqp://guest@localhost//')


@shared_task
def mailing_mail(request):
    form = MailingForm()
    if request.method == 'POST' and request.is_ajax():
        form = MailingForm(request.POST)
        if form.is_valid():
            users = User.objects.all()
            for i in users:
                text = form.cleaned_data['text']

                mail = Mail.create(user=i)
                text += '\n Так же просим вас перейти по данной ссылке, чтобы мы могли получить обратную информацию ' \
                        'от вас: http://127.0.0.1:8000/{}'.context(
                    mail.id)
                mail.text = text
                mail.save()
                i.mails.add(mail)
                i.save()
                send_mail(message=text, recipient_list=i.email)
            return JsonResponse('Отправка рассылки произошла успешно')
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)
    return render(request, 'index.html', {form: form})


def confirmation_of_the_transition(request, pk):
    mail = Mail.objects.get(id=pk)
    mail.status = True
    mail.save()
    return render(request, 'confirm.html')
