from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *

import copy
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
    def get(self, request,id):
        
       
        comments_list = []
        comment_dict =[]
        user = request.user
        comments_list.append([user.picture.url,user.id])
        comments = Comment.objects.filter(project=id)
        for comment in comments:
            user_profile = User.objects.get(id=comment.user.id)
            comment_dict.append( {
                'id': comment.id,  # Include the comment ID or any other fields you need
                'fname': user_profile.fname,
                'user_photo': user_profile.picture.url,
                'content': comment.content,
                # 'parent':comment.parent,
                'created_at': comment.created_at,
                'parent': comment.parent.id if comment.parent else None,  # Check if the comment has a parent
            })
            
        # Add the comment dictionary to the list
        comments_list.append(comment_dict)
        
        return JsonResponse(comments_list, safe=False, status=status.HTTP_200_OK)
        # return JsonResponse({comments}, status=status.HTTP_200_OK)
        

class ReplyAPIView(APIView):
   
    def post(self, request):
        content = request.data.get('contents')
        
        comment_id = request.data.get('id')
        comment = Comment.objects.get(id=comment_id)
        user = request.user
        
        comment = Comment.objects.create(
            content=content,
            project=comment.project,
            user=user,
            parent=comment
        )
        return Response({'state': 'success'}, status=status.HTTP_201_CREATED)
class RateAPIView(APIView):
    def post(self, request):
        rate = request.data.get('rate')
        user = request.user
        project_id = request.data.get('id')
        if Rating.objects.filter(user=user.id,project=project_id ).exists():
            current_rete = Rating.objects.get(user=user.id,project=project_id )
            current_rete.value = rate
            current_rete.save()
        else :
            project = Project.objects.get(id=project_id)
            new_rate = Rating.objects.create(
                user=user,
                project=project,
                value=rate
            )
        return Response({'state': 'success'}, status=status.HTTP_201_CREATED)
    def get(self, request, id):
        rates = Rating.objects.filter(project=id)
        rate_list = []
        for rate in rates:
            user_profile = User.objects.get(id=rate.user.id)
            rate_list.append({
                'id': rate.id,
                'fname': user_profile.fname,
                'user_photo': user_profile.picture.url,
                'rate': rate.value
            })
       
        return JsonResponse(rate_list, safe=False, status=status.HTTP_200_OK)

class Report_Comment_Project(APIView):
    def post(self, request):
        report_type=request.data.get('type')
        if report_type == 'Comment':
            content = request.data.get('content')
            comment_id = request.data.get('id')
            comment = Comment.objects.get(id=comment_id)
            user = request.user
            report = Report.objects.create(
            reason=content,
            report_type='comment',
            user=user,
            comment=comment
            )
            return Response({'state': 'success'}, status=status.HTTP_201_CREATED)
        elif report_type == 'Project':
            content = request.data.get('content')
            print
            project_id = request.data.get('id')
            print(project_id)
            project = Project.objects.get(id=project_id)
            user = request.user
            report = Report.objects.create(
            reason=content,
            report_type='project',
            user=user,
            project=project
            )
            return Response({'state': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid type'}, status=status.HTTP_400_BAD_REQUEST)
        

