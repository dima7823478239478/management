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
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_manager/', views.main_manager_view, name='main_manager'),# Главная страница менеджера
    path('main_user/', views.main_user_view, name='main_user'),# Главная страница пользователя
    path('', views.login_view, name='login'),  # Вход
    path('logout/', views.logout_view, name='logout'),  # Кастомный выход
    path('statistics/', views.statistics_view, name='statistics'),# статистика
    path('main_manager/add_user', views.add_user_view, name='add_user'),# Страница добавления пользователя
    path('edit_user/<int:worker_id>/', views.edit_user, name='edit_user'),  # Страница редактирования пользователя
    path('search_worker/', views.search_worker, name='search_worker'),  # Страница поиска работника
    path('main_manager/offer_list', views.offer_list, name='offer_list'),# Страница просмотра заказов
    path('main_manager/add_offer/', views.add_offer, name='add_offer'),# Страница добавления заказа
    path('delete_user/<int:worker_id>/', views.delete_user, name='delete_user'),
    path('statistics/<int:id>/', views.statistics_view, name='statistics_detail'),# Страница просмотра статистики работника
    path('worker/<int:worker_id>/', views.worker_statistics, name='worker_statistics'),


]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
