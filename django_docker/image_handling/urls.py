from django.urls import path
from . import views

app_name = 'image_handling'

urlpatterns = [
    # URL patterns for image upload and messaging views
    # Example:
    path('upload/', views.upload_image, name='upload'),
    path('send/', views.send_image, name='send'),
    #path('media/<str:username>/uploaded/', views.serve_uploaded_images, name='serve_uploaded_images'),
    path('media/<str:username>/uploaded/', views.get_all_images, name='get_all_images'),
    path('media/<str:username>/latest', views.latest_image, name='latest'),
    path('media/<str:username>/uncropped_image', views.fetch_uncropped_image, name='latest'),
    path('save_cropped_image/<str:selected_user>/', views.save_cropped_image, name='save_cropped_image'),
    path('<str:selected_user>/crop/', views.display_image_cropping_page, name='crop'),
    path('delete/<str:username>/<str:image>/', views.Delete_uploaded_image, name='delete'),
    
   # path('send/', views.send_message, name='send'),
]