from django.shortcuts import render ,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.views import View
from users.models import User ,User_active
import random
import string
from datetime import datetime, timedelta

class login(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            return render(request, 'users/login.html', {'error': 'Account not exists.'})
        password = request.POST.get('password')
        current_user= User.objects.get(email=email)
        if password == current_user.password:
            if current_user.active_email == False:
                return redirect('active', current_user.id)
            
            login_authuser=authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            if(current_user is not None and login_authuser):
            ##sesion
                request.session['id']=current_user.id
                request.session['name']=current_user.fname
                login(request)
                
                return redirect('')
        else:
            return render(request, 'users/login.html')

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
        return redirect('active', user.id)
def activation(request, id, activation_code):
    user = User.objects.get(id=id)
    use_active=User_active.objects.get(user=user)
    if (use_active.active == activation_code & use_active.time_send -datetime.now() < timedelta(days=1)):
        user.active_email = True
        user.save()
        return render(request, 'users/active.html',{'message': 'Your account has been activated successfully.'})

    return render(request, 'users/active.html',{'error': 'Activation link is invalid or expired.'})

def active(request,id):
    user = User.objects.get(id=id)
    activation_code = User_active.objects.get(user=user).active
    subject = 'Account Activation'
    message = f'Your activation link is: http://127.0.0.1:8000/users/{user.id}/{activation_code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    return render(request, 'users/active.html',{'message': 'Please check your email to activate your account.'})

    




def logout(request):
    request.session.clear()
    logout(request)
    return redirect('users')
