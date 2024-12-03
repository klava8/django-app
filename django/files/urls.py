from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('upload/', views.upload_file, name='upload_file'),
  path('upload_chunk/', views.upload_chunk, name='upload_chunk'),
  path('download/<int:file_id>/', views.download_file, name='download_file'),
  path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]

