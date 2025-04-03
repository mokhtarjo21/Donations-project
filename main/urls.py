from .views import HomePage
from django.urls import path

urlpatterns = [
    path('', HomePage.as_view(), name='home'),


    # TODO: Add Views fo thes

    # path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_details'),
    # path('project/<int:pk>/donate/', DonateView.as_view(), name='donate'),
]