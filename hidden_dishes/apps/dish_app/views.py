from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from ..login_app.models import Client
from .models import Plate, Restaurant, Comment, Like
from django.contrib import messages

# Create your views here.
def index(request):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    user = Client.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'plates': Plate.objects.all().order_by('-created_at'),
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

    user = Client.objects.get(id=id)
    context = {
        'user': user,
        'plates': Plate.objects.filter(user_id=id).order_by('-created_at'),
    }
    return render(request, 'dish_app/profile.html', context)

def add_dish(request):
    if request.method == 'POST':
        result_plate = Plate.objects.plate_validator(request.POST)
        result_restaurant = Restaurant.objects.restaurant_validator(request.POST)

        if result_plate[0] == False or result_restaurant[0] == False:
            for error in result_plate[1]:
                messages.error(request, error, extra_tags="plate")
            for error in result_restaurant[1]:
                messages.error(request, error, extra_tags="restaurant")
            return redirect(reverse('dish:add'))
        else:
            restaurant = Restaurant.objects.create(name=request.POST['restaurant'])

            context = {
                'user': Client.objects.get(id=request.session['user_id']),
                'restaurant': restaurant,
                'name': request.POST['plate'],
                'review': request.POST['review'],
            }
            Plate.objects.create(**context)
            return redirect(reverse('dish:index'))

def show_plate(request, id):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    plate = Plate.objects.get(id=id)
    comments = Comment.objects.filter(plate=plate)
    context = {
        'user': Client.objects.get(id=request.session['user_id']),
        'plate': plate,
        'comments': comments,

    }
    return render(request, 'dish_app/plate.html', context)

def restaurant(request, id):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    context = {
        'user': Client.objects.get(id=request.session['user_id']),
        'restaurant': Restaurant.objects.get(id=id),
    }
    return render(request, 'dish_app/restaurant.html', context)

def top(request):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    context = {
        'user': Client.objects.get(id=request.session['user_id']),
    }
    return render(request, 'dish_app/top.html', context)

def add_comment(request, id):
    if request.method == "POST":
        result = Comment.objects.comment_validator(request.POST, request.session['user_id'], id)

        if result[0] == True:
            messages.success(request, "Successfully added comment")
            return redirect(reverse('dish:show_plate', kwargs={'id': id}))
        else:
            for errors in result[1]:
                messages.error(request, errors, extra_tags="comments")
                return redirect(reverse('dish:show_plate', kwargs={'id': id}))
