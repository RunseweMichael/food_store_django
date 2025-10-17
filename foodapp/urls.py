from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('allusers/', views.allusers, name='allusers'),
    path('delete/<int:id>', views.deleteuser, name='deleteuser'),
    path('update/<int:id>', views.updateuser, name='updateuser'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
