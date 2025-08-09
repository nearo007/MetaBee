from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('printers', views.printers, name="printers"),
    path('door-lock', views.door_lock, name="door-lock"),
]