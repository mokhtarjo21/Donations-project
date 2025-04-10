
from django.contrib import admin
from django.urls import path , include
# to show the images in development mode 
from django.conf import settings
from django.conf.urls.static import static


# from users.views import *
from main.views import *
urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path ('chat', include('chatgpt.urls')),
    path ('users/', include('users.urls')),
    path ('dashboard/', include('dashboard.urls')),
    path ('interactions', include('interactions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
