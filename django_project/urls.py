
from django.contrib import admin
from django.urls import path , include
# from users.views import *
from main.views import *
urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    # path('/', include('main.urls')),
    path ('chat', include('chatgpt.urls')),

   
]
