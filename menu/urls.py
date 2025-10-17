from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/create/', views.create_menu_item, name='create_menu_item'),
    path('menu/delete/<int:id>/', views.delete_menu_item, name='delete_menu_item'),
    path('menu/update/<int:id>/', views.update_menu_item, name='update_menu_item'),
]