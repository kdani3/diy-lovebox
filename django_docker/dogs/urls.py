from django.urls import path
from . import views

app_name = 'dogs'

urlpatterns = [
    # URL patterns for image upload and messaging views
    path('', views.dogs, name='dogs'),
   # path('send/', views.send_message, name='send'),
]