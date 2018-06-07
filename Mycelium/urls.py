"""Mycelium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path

from api import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('users-list/', views.UsersListView.as_view(), name='users-list'),
    path('contacts-list/', views.ContactsListView.as_view(), name='contacts-list'),
    path('user-edit/', views.UserEditView.as_view(), name='user-edit'),
]
