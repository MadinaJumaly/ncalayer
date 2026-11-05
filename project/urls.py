"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app.views import index
from users import views
from documents.views import my_view
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from ncalogin.views import ncalayer_login
from ncalogin.views import login_page, ncalayer_login
from django.contrib.auth.views import LogoutView
from documents.views import my_view, sign_document, send_email_view
urlpatterns = [
    path("admin/", admin.site.urls),
    # =path("", user),
    path("index/", index),
    path('api/ncalayer-login/', ncalayer_login, name='ncalayer_login'),
    path('login/', login_page, name='login'),
    path("logout/", views.logoutuser, name="logoutuser"),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documents/', my_view, name='my-view') ,
    path('sign/', sign_document, name='sign-document'),
    path('send_email/', send_email_view, name='send-email'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
