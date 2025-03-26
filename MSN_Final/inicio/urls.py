from django.urls import path
from .views import password_reset_request, verify_code, set_new_password
from . import views

app_name = 'inicio'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.registro, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('verify-code/', verify_code, name='verify_code'),
    path('set-new-password/', set_new_password, name='set_new_password'),
]
