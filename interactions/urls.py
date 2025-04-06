from .views import *
from django.urls import path , include

urlpatterns = [
    path('', CommentAPIView.as_view(), name='CommentView'),
    path('<int:comment_id>/reply/', ReplyAPIView.as_view(), name='comment-reply'),
    # path('reply', ReplyView.as_view(), name='reply'),
    # path('rate', RateView.as_view(), name='rate'),
]
