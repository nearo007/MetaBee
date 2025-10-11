from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('manage_printers', views.manage_printers, name="manage_printers"),
    path('add_printer', views.add_printer, name="add_printer"),
    path('delete_printer/<int:printer_id>', views.delete_printer, name="delete_printer")
]