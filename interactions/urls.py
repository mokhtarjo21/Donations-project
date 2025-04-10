from .views import *
from django.urls import path , include

urlpatterns = [
    path('', CommentAPIView.as_view(), name='CommentView'),
    path('/<int:id>', CommentAPIView.as_view(), name='CommentView'),
    path('/reply', ReplyAPIView.as_view(), name='comment-reply'),
    path('/rate/<int:id>', RateAPIView.as_view(), name='rate'),
    path('/rate', RateAPIView.as_view(), name='rate'),
     path('/report', Report_Comment_Project.as_view(), name='Report_Comment_Project'),
]
