from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .scrapers import scrape
from django.http import HttpResponse, JsonResponse
from .models import MyDashOne, ScrapedData
from time import sleep

import random

# Create your views here.

# send_email_change_request(request.user,
#                                   form.cleaned_data['email'],
#                                   https=request.is_secure())

login_url = "https://mydash.one"
activityLogUrl = "https://mydash.one/rlogs/line"
resetPass = False

@login_required
def dashboard(request):
    if request.method == "POST":
        enginhealth = MyDashOne.objects.all()[0]
        val = enginhealth.engineIsSafe
        return JsonResponse({'enginehealth': val})
    return render(request, 'dashboard.html')

def forCheck(request, email, password):
    us = ''
    try:
        us = User.objects.get(email=email).username
    except: pass
    user = authenticate(request, username=us, password=password)
    return user

def to_login(request):
    global resetPass
    print({'resetPass value: ': resetPass})
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('pswd')
        print(email, password)
        # print(request.POST['email'])
        user = forCheck(request, email, password)
        if user != None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'authentication/login.html', {'status': 1})
    resetPass = False
    return render(request, 'authentication/login.html')

@login_required
def to_settings(request):
    if request.POST:
        print(request.POST['form_type'])
        if request.POST['form_type'] == 'scraper':
            femail, fpassword = request.POST['formData[fscrapemail]'], request.POST['formData[fscrappassword]']
            nemail, npassword = request.POST['formData[nscrapemail]'], request.POST['formData[nscrappassword]']
            print(femail, fpassword)
            user = forCheck(request, femail, fpassword)
            if user and (request.user.email == femail):
                u = User.objects.get(email=femail)
                u.set_password(npassword)
                u.save()
                return HttpResponse({'messages': 'successfully changed!'})
            return HttpResponse({'messagef': 'password failed, check formal password!'})

        elif request.POST['form_type'] == 'mydash':
            print(request.POST)
            username, fpassword = request.POST['formData[mydashusername]'], request.POST['formData[mydashpswd]']
            npassword = request.POST['formData[mydashnpswd]']
            mydashUser = MyDashOne.objects.filter(username=username, password=fpassword)
            print(mydashUser)
            if mydashUser.exists():
                print('hi')
                dash_user = MyDashOne(username=username, password=fpassword)
                dash_user.password = npassword
                dash_user.save()
                return HttpResponse({'messages': 'successfully changed!'})
            return HttpResponse({'messagef': 'password failed, check formal password!'})
    return render(request, 'settings.html')

@login_required
def allusers(request):
    global login_url, activityLogUrl
    if request.method == 'GET':
        # login_url = "https://mydash.one"
        # activityLogUrl = "https://mydash.one/rconnections"
        # scrape(login_url, activityLogUrl)
        pass

    if request.method == 'POST':
        userData = ScrapedData.objects.all().values()
        return JsonResponse({'data': list(userData)})
    
    return render(request, 'users.html', {'data': [1, 2]})

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).exists()
        code = random.randrange(1000, 9999)
        if user:
            o = User.objects.get(email=email)
            send_mail(
                subject='Scraper Password Reset Code',
                message=f'this is your code {str(code)}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['drjerrypro@gmail.com']
            )
            try:
                o.last_name = str(code)
                o.save()
                return redirect('reset_password', email)
            except:
                print("could not send mail, try again...")
                return render(request, 'authentication/forgot-password.html', {'status': 2})
        return render(request, 'authentication/forgot-password.html', {'status': 1})
    return render(request, 'authentication/forgot-password.html')

def reset_password(request, email):
    # if request.GET['']
    global resetPass
    if request.method == "POST":
        code = request.POST.get('code')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            code_db = str(user.last_name)
            print({'code': code, "code_db": code_db})
            if code == code_db:
                print("accepted code is true...")
                user.set_password(password)
                user.save()
                user.last_name = ''
                user.save()
                # post = request.POST.copy()
                # post["email"] = email
                # post["pswd"] = passw
                resetPass = True
                return redirect('login')
            return render(request, 'authentication/password-reset.html', {'status': 1})
        except:
            return render(request, 'authentication/password-reset.html', {'status': 1})
    
    return render(request, 'authentication/password-reset.html')