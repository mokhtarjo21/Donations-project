from .views import *
from django.urls import path

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('profile/', ProfilePage.as_view(), name='profile'),
    path('editprofile/', EditProfile.as_view(), name='edit_profile'),
    path('donation_history/', DonationHistory.as_view(), name='donation_history'),
    path('my-projects/', UserProjects.as_view(), name='user_projects'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('donate/<int:pk>/', donate_view, name='donate'),

    # TODO: Add Views fo thes

    # path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_details'),
    # path('project/<int:pk>/donate/', DonateView.as_view(), name='donate'),
]