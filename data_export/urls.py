from django.urls import path
from . import views

app_name = 'data_export'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/databases/', views.get_databases, name='get_databases'),
    path('api/collections/', views.get_collections, name='get_collections'),
    path('api/fields/', views.get_fields, name='get_fields'),
    path('api/export/', views.export_data, name='export_data'),
]