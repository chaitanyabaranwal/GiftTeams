"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from boards import views
from boards.forms import SignInForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('', auth_views.LoginView.as_view(template_name='signin/signin.html', authentication_form=SignInForm), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('home/', views.home, name='home'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:team_id>', views.view_team, name='view_team'),
    path('teams/new', views.create_team, name='create_team'),
    path('teams/<int:team_id>/edit', views.edit_team, name='edit_team'),
    path('teams/<int:team_id>/delete', views.delete_team, name='delete_team'),
    path('persons/new', views.create_person, name='create_person'),
    path('persons/<int:person_id>/edit', views.edit_person, name='edit_person'),
    path('persons/<int:person_id>/delete', views.delete_person, name='delete_person')
]
