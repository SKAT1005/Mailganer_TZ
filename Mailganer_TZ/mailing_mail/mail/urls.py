from django.urls import path
from views import confirmation_of_the_transition, mailing_mail

urlpatterns = [
    path('', mailing_mail, name='mailing_mail'),
    path('<int:pk>', confirmation_of_the_transition, name='confirmation_of_the_transition'),
]
