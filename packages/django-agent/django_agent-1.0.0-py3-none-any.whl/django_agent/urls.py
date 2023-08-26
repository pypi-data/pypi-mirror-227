from django.urls import path
from . import views

urlpatterns = [
    path('shell', views.shell, name='shell'),
    path('info', views.info, name='info'),
]