"""
URL configuration for work_control project.

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
from django.urls import path, include
from app1 import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_manager/', views.main_manager_view, name='main_manager'),
    path('main_user/', views.main_user_view, name='main_user'),
    path('', views.login_view, name='login'),  # Вход
    path('logout/', views.logout_view, name='logout'),  # Кастомный выход
    path('statistics/', views.statistics_view, name='statistics'),
    path('main_manager/add_user', views.add_user_view, name='add_user'),
    path('edit_user/<int:worker_id>/', views.edit_user, name='edit_user'),  # Страница редактирования
    path('search_worker/', views.search_worker, name='search_worker'),  # Страница редактирования
    path('main_manager/add_task', views.add_task_view, name='add_task'),
    path('main_manager/edit_task', views.edit_task_view, name='edit_task'),
    path('main_manager/user_delete', views.user_delete, name='user_delete'),
    path('statistics/<int:id>/', views.statistics_view, name='statistics_detail'),
    path('worker/<int:worker_id>/', views.worker_statistics, name='worker_statistics'),
    path('magazine/', views.magazine_view, name='magazine'),

]
