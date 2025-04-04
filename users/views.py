from django.shortcuts import render ,redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from chatgpt.models import ChatMessage
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import AnonymousUser
from django.views import View
from users.models import User ,User_active
import random
import string
from datetime import datetime, timedelta


from django.http import JsonResponse
import json
from openai import OpenAI ,RateLimitError
from rest_framework.decorators import api_view


class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            return render(request, 'users/login.html', {'error': 'Account does not exist.'})
        
        password = request.POST.get('password')
        current_user = User.objects.get(email=email)
        
        if password == current_user.password:
            if not current_user.active_email:
                return redirect('active', current_user.id)
            
            login(request, current_user)
            return redirect('/')
        else:
            return render(request, 'users/login.html', {'error': 'Email or password is incorrect.'})

class register(View):
    def get(self, request):
        return render(request, 'users/signup.html')

    def post(self, request):
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        picture = request.FILES.get('picture')

        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/signup.html', {'error': 'Account already exists.'})

        user = User(fname=fname, lname=lname, email=email, password=password, picture=picture, phone=phone)
        user.save()
        activation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        User_active.objects.create(user=user, active=activation_code)
        
        return redirect(f'active/{user.id}')
def activation(request, id, activation_code):
    user = User.objects.get(id=id)
    use_active=User_active.objects.get(user=user)

    if (use_active.active == activation_code and now() - use_active.time_send < timedelta(days=1)):
        user.active_email = True
        user.save()
        return render(request, 'users/active.html',{'message': 'Your account has been activated successfully.'})

    return render(request, 'users/active.html',{'message': 'Activation link is invalid or expired.'})

def active(request,id):
    user = User.objects.get(id=id)
    use_active = User_active.objects.get(user=user)
    if (now() - use_active.time_send > timedelta(days=1)):
        activation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        use_active = User_active.objects.get(user=user)
        use_active.active = activation_code
        use_active.time_send = now()
        use_active.save()

    activation_code = User_active.objects.get(user=user).active
    subject = 'Account Activation'
    message = f'Your activation link is: http://127.0.0.1:8000/users/{user.id}/{activation_code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    return render(request, 'users/active.html',{'message': 'Please check your email to activate your account.'})

    



def logout_view(request):
    logout(request)
    return redirect('/users/')  # Ensure the path matches your login URL


@api_view(['GET'])
def who(request):
    userw = request.user
    if isinstance(userw, AnonymousUser):
        return JsonResponse({'response':{'state': False}})
    else:
        user_data = {
            'state': True,
            'id': userw.id,
            'email': userw.email,
            'first_name': userw.first_name,
            'last_name': userw.last_name,
            'fname': userw.fname,
            'lname': userw.lname,
            'pciture': userw.picture.url if userw.picture else None
        }
        return JsonResponse({'response': user_data})
     
