from django.urls import path
from . import views
from django.contrib.auth.views import LoginView



app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True,template_name='accounts/login.html'), name='login'),
]