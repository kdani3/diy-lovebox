from django.urls import path
from . import views

app_name = 'cats'

urlpatterns = [
    # URL patterns for image upload and messaging views
    path('', views.cats, name='cats'),
   # path('send/', views.send_message, name='send'),
]