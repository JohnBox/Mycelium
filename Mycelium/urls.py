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
from django.views.generic import RedirectView

from api import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('users-list/', views.UsersListView.as_view(), name='users-list'),
    path('user-edit/', views.UserEditView.as_view(), name='user-edit'),
    path('contacts-list/', views.ContactsListView.as_view(), name='contacts-list'),
    path('create-contact/', views.CreateContactView.as_view(), name='create-contact'),
    path('delete-contact/', views.DeleteContactView.as_view(), name='delete-contact'),
    path('create-group/', views.CreateGroupView.as_view(), name='create-group'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),

    path('users/', views.UserList.as_view(), name='users'),
    path('groups/', views.GroupList.as_view(), name='groups'),
]
