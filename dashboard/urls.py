from .views import *
from django.urls import path , include



from main.views import HomePage
from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path('', category_list, name='category_list'),
    path('categories/add/',category_create, name='category_add'),
    path('categories/edit/<int:pk>/',category_update, name='category_edit'),
    path('categories/delete/<int:pk>/',category_delete, name='category_delete'),
    path('projects/', project_list, name='project_list'),
    path('projects/add/', project_create, name='project_add'),
    path('projects/<int:pk>/edit/', project_edit, name='project_edit'),
     path('projects/<int:pk>/delete/', project_delete, name='project_delete'),

]