from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


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
        try:
            comment = Comment.objects.get(pk=pk, user=request.user)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete an existing comment.
        """
        try:
            comment = Comment.objects.get(pk=pk, user=request.user)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReplyAPIView(APIView):
   
    def post(self, request, comment_id, *args, **kwargs):
        """
        Reply to an existing comment.
        """
        try:
            parent_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a new comment and set the parent as the provided comment ID
        data = request.data.copy()
        data['parent'] = parent_comment.id  # Set the parent field to the parent comment's ID
        serializer = CommentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically set the user as the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
