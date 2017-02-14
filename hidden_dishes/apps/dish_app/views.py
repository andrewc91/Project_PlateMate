from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from ..login_app.models import Client
from .models import Plate, Restaurant, Comment
from django.contrib import messages
from django.db.models import Count

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
    comments = Comment.objects.filter(plate=Plate.objects.get(id=id)).order_by('-created_at')
    context = {
        'user': Client.objects.get(id=request.session['user_id']),
        'plate': plate,
        'comments': comments,
        'likes': Plate.objects.annotate(total_like=Count('likes')),

    }
    return render(request, 'dish_app/plate.html', context)

def top(request):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))

    context = {
        'user': Client.objects.get(id=request.session['user_id']),
        'plates': Plate.objects.annotate(total_like=Count('likes')).order_by('-total_like')
    }
    return render(request, 'dish_app/top.html', context)

def add_comment(request, id):
    if request.method == "POST":
        result = Comment.objects.comment_validator(request.POST, request.session['user_id'], id)

        if result[0] == True:
            return redirect(reverse('dish:show_plate', kwargs={'id': id}))
        else:
            for errors in result[1]:
                messages.error(request, errors, extra_tags="comments")
                return redirect(reverse('dish:show_plate', kwargs={'id': id}))

def delete(request, id):
    Plate.objects.get(id=id).delete()
    return redirect(reverse('dish:index'))

def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect(reverse('dish:show_plate', kwargs={'id':comment.plate.id}))

def like(request, id):
    # user = Client.objects.get(id=request.session['user_id'])
    Plate.objects.add_like(request.session['user_id'], id)
    return redirect(reverse('dish:show_plate', kwargs={'id':id}))
