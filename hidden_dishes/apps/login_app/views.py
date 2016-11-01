from django.shortcuts import render, redirect
from .models import Client
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect(reverse('dish:index'))
    else:
        return render(request, 'login_app/index.html')

def register(request):
    return render(request, 'login_app/register.html')

def aboutme(request):
    return render(request, 'login_app/aboutme.html')

def process(request):
    result = Client.objects.register(request.POST)
    if result[0] == True:
        request.session['user_id'] = result[1].id
        messages.success(request, "Hello! You have successfully registered!")
        return redirect(reverse('dish:index'))
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect(reverse('login:register'))

def login(request):
    result = Client.objects.login(request.POST)
    if result[0] == True:
        request.session['user_id'] = result[1].id
        return redirect(reverse('dish:index'))
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect(reverse('login:index'))

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "You have been successfully logged out")
        return redirect(reverse('login:index'))
