from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list, name='category_list'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('category/delete/<int:id>/', views.deletecategory, name='deletecategory'),
    path('category/update/<int:id>/', views.updatecategory, name='updatecategory'),
]