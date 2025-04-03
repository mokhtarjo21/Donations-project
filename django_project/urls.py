
from django.contrib import admin
from django.urls import path , include
from users.views import *
urlpatterns = [
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('home/', include('users.urls')),
    path ('chat', include('chatgpt.urls')),
    # path ('projects', include('projects.urls')),
    # path ('catogery', include('catogery.urls')),
    # path ('commentes', include('commentes.urls')),
    # path ('reports', include('reports.urls')),
    # path ('users', include('users.urls')),
    path ('login/', login.as_view(), name='login'),
    path ('register/', register.as_view(), name='register'),
    # path ('logout', logout_view, name='logout'),
   
]
