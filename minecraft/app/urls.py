 
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page),
    path('step2', views.form_page),
    path('step3', views.calculating)
]
