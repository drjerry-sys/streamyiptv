"""webScraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from scraper.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', to_login, name='login'),
    path('settings/', to_settings, name='settings'),
    path('dashboard/', dashboard, name='dashboard'),
    path('users/', allusers, name='users'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:email>/', reset_password, name='reset_password'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
