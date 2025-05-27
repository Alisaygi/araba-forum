from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/add/', views.add_car, name='add_car'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('cars/<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:pk>/delete/', views.delete_car, name='delete_car'),
    path('cars/statistics/', views.car_statistics, name='car_statistics'),
    path('reviews/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('my-news/', views.my_news, name='my_news'),
    path('news/edit/<int:pk>/', views.edit_news, name='edit_news'),
    path('news/delete/<int:pk>/', views.delete_news, name='delete_news'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('settings/', views.user_settings, name='settings'),
] 