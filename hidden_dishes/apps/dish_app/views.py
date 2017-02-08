from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from ..login_app.models import Client
from django.contrib import messages

# Create your views here.
def index(request):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    user = Client.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'dish_app/index.html', context)

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "You have been successfully logged out")
        return redirect(reverse('login:index'))

def add(request):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    user = Client.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }

    return render(request, 'dish_app/add_plate.html', context)

def profile(request, id):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    user = Client.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'dish_app/profile.html', context)

def add_dish(request):
    if request.method == 'POST':
        return redirect(reverse('dish:index'))
