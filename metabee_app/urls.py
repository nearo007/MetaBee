from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('manage_printers', views.manage_printers, name="manage_printers"),
    path('add_printer', views.add_printer, name="add_printer"),
    path('delete_printer/<int:printer_id>', views.delete_printer, name="delete_printer"),
    path('get_printers_state', views.get_printers_state, name="get_printers_state"),
    path('api/get_printer_status_id/<str:device_id>', views.api_get_printer_status_id, name="api_get_printer_status_id"),
    path('api/get_printer_status_name/<str:printer_name>', views.api_get_printer_status_name, name="api_get_printer_status_name")
]