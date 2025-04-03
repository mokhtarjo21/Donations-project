
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
    # path('/', include('main.urls')),
    path ('chat', include('chatgpt.urls')),
    path ('users/', include('users.urls')),
]
if settings.DEBUG:  # Serve media files in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
