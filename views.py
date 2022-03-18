

from typing import NewType
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.

def index (request):
    return render(request, 'logreg.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/wishes')

def login(request):
    user = User.objects.filter(email=request.POST['email']) 
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
    return redirect('/wishes')


def wishes (request):
    context = {
        'wishes': Wish.objects.all()
    }
    return render(request, 'wishes.html', context)

def new_wish(request):
    return render(request, 'new.html')

def create_wish(request, user_id):
    poster = User.objects.get(id=request.session['user_id'])
    new_wish= Wish.objects.get(id=id)
    Wish.objects.create(new_wish=request.POST['new_wish'], poster=poster,description = request.POST['description'])
    return redirect('/wishes')


def show_one(request, wish_id):
    context = {
        'wish': Wish.objects.get(id=wish_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'wishes/stats.html', context)


def add_like(request, user_id):
    liked_wish = Wish.objects.get(id=user_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_wish.user_likes.add(user_liking)
    return redirect('/wishes')


def edit(request, wish_id):
    one_wish = Wish.objects.get(id=wish_id)
    context = {
        'wish': one_wish
    }
    return render(request, 'edit.html', context)

def update(request, wish_id):
    # update wish!
    to_update = Wish.objects.get(id=wish_id)
    # updates each field
    to_update.new_wish = request.POST['new_wish']
    to_update.description = request.POST['description']
    to_update.save()
    return redirect(f"/wishes/{wish_id}")


def delete(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.delete()
    return redirect('/wishes')

def logout(request):
    request.session.flush()
    return redirect('/')




