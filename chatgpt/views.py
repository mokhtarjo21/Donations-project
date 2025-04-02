from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from openai import OpenAI
from openai import RateLimitError
from rest_framework.decorators import api_view


@api_view(['POST'])
def api_request_response(request):
     message = request.data.get('message')
     try:
        client = OpenAI(api_key="your_api_key_here")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}],
            
        )
        response = completion.choices[0].message.content
        print(response)
        return JsonResponse({'response': response})
     except RateLimitError:
        return JsonResponse({'error': 'You have exceeded your API quota. Please check your OpenAI plan.'}, status=429)
