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
    # path('admin_dashboard', AdminDashboardView.as_view(), name='admin_dashboard'),
    # path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard', AdminDashboardView.as_view(), name='admin_dashboard'),
    # path('edit_user_data', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('export-users/', export_users_csv, name='export_users'),

    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    
]