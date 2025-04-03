from users.views import *
from django.urls import path , include

urlpatterns = [
    path('', login.as_view(), name='login'),
    path('register', register.as_view(), name='register'),
    path('logout', logout.as_view(), name='logout'),
    path ('<int:id>/<str:activation_code>', activation, name='activate'),
    path('active/<int:id>', active, name='active'),
    
  
]
