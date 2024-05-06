from django.urls import path
from . import views

app_name = 'releases'

urlpatterns = [
    # URL patterns for image upload and messaging views
    path('', views.releases, name='releases'),
    path('upload_release/', views.upload_release, name='upload_release'),
    path('<str:filename>/', views.download_release, name='download_release'),
    path('<path:filename>/', views.download_release, name='download_release'),



   # path('send/', views.send_message, name='send'),
]