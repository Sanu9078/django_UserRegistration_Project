"""
URL configuration for UserRegistration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/',register,name='register'),
    path('user_login/',user_login,name='user_login'),
    path('user_profile',user_profile,name='user_profile'),
    path('',home,name='home'),
    path('logout',logout_view,name='logout'),
    path('change_password',change_password,name='change_password'),
    path('otp',otp,name='otp'),
    path('forget_password',forget_password,name='forget_password'),
    path('forget_password_username',forget_password_username,name='forget_password_username'),
    path('forget_otp',forget_otp,name='forget_otp')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
