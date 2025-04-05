from .views import *
from django.urls import path , include



from main.views import HomePage
from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path('', category_views.category_list, name='category_list'),
    path('categories/add/', category_views.category_create, name='category_add'),
    path('categories/edit/<int:pk>/', category_views.category_update, name='category_edit'),
    path('categories/delete/<int:pk>/', category_views.category_delete, name='category_delete'),
    path('projects/', project_views.project_list, name='project_list'),
    path('projects/add/', project_views.project_create, name='project_add'),

]