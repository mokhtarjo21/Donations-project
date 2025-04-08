from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


from django.http import JsonResponse
import json

class CommentAPIView(APIView):
   
    def post(self, request):
        content = request.data.get('contents')
        print(content,'content')
        project_id = request.data.get('id')
        project = Project.objects.get(id=project_id)
        user = request.user
        print(user,'user')
        # Create a new comment
        comment = Comment.objects.create(
            content=content,
            project=project,
            user=user
        )
        return Response({'state': 'success'}, status=status.HTTP_201_CREATED)
    def put(self, request, pk, *args, **kwargs):
        """
        Update an existing comment.
        """
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete an existing comment.
        """
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get(self, request):
        
        comments_list = []
        user = request.user
        comments_list.append([user.picture.url,user.id])
        comments = Comment.objects.all()
        comments_list.append(list(comments.values()) )
        users = User.objects.all()
        comments_list.append(list(users.values()))
       
        # comments_list.append() # Convert to a list of dictionaries
        return JsonResponse(comments_list, safe=False, status=status.HTTP_200_OK)
        # return JsonResponse({comments}, status=status.HTTP_200_OK)
        

class ReplyAPIView(APIView):
   
    def post(self, request):
        content = request.data.get('contents')
        print(content,'content')
        comment_id = request.data.get('id')
        comment = Comment.objects.get(id=comment_id)
        user = request.user
        print(user,'user')
        comment = Comment.objects.create(
            content=content,
            project=comment.project,
            user=user,
            parent=comment
        )
        return Response({'state': 'success'}, status=status.HTTP_201_CREATED)