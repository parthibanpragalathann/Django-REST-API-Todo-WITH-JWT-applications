from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, UpdateUserView, DeleteUserView, PasswordView, \
    TaskListView, TaskDetailView, \
    CompletedTask, PaginatedTask, Profile, LoggedInUserView
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r"user/me/avatar", Profile, basename="profile")#7
router.register(r"user/me/avatar/<int:pk>", Profile, basename="profile")#8

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='auth_register'),#1-
    path('user/login/', LoginView.as_view(), name='auth_login'),#2-
    path('user/me/', LoggedInUserView.as_view(), name='auth_user'),#3-
    path('user/me/<int:pk>/', UpdateUserView.as_view(), name='auth_update'),#4
    path('user/me/delete/<int:pk>/', DeleteUserView.as_view(), name='auth_delete'),#5
    path('user/password/<int:pk>/', PasswordView.as_view(), name='auth_change_password'),#6
    path('task/', TaskListView.as_view(), name='task_list'),#9
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_details'),#10
    path('task/completed/', CompletedTask.as_view(), name='task_completed'),#11
    path('', include(router.urls)),#7 #8
    path('user/refresh/token/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('user/logout/', LogoutView.as_view(), name='auth_logout'),
    path('task/pagination/', PaginatedTask.as_view(), name='task_paginated'),
]