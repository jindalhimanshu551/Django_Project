from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    username = request.user.username
    queryset = todo.objects.filter(
        user__username=username)
    
    task_completed_query = todo.objects.filter(
        user__username=username,
        completed=True,
    )

    for task in task_completed_query:
        if (task.one_day_ago() and task.completed == True):
             task.delete()
             
    context = {
        'todos' : queryset
    }
    return render(request,"index.html",context)

@login_required(login_url='/login/')
def add_task(request):
    if request.method == "POST":
        data = request.POST

        user = request.user
        title = data.get('title')
        description = data.get('description')
        

        todo.objects.create(
            user=user,
            title=title,
            description=description,
        )

        return redirect('/todo/')

    return render(request,"add_task.html")

@login_required(login_url='/login/')
def update_task(request, task_id):
    task = get_object_or_404(todo, pk=task_id)
    if request.method == "POST":
        data = request.POST

        title = data.get('title')
        description = data.get('description')
        completed = data.get('completed') == 'on'

        task.title = title
        task.description = description

        if completed:
            task.completed = completed
        else:
            task.completed = completed

        task.save()

        return redirect('/todo/')
    
    context = {
        'task' : task
    }
    return render(request,"update_task.html",context)

@login_required(login_url='/login/')
def mark_as_completed(request, task_id):
    task = get_object_or_404(todo, pk=task_id)
    task.completed = True
    task.save()

    return redirect('/todo/')

@login_required(login_url='/login/')
def delete_task(request, task_id):
    task = get_object_or_404(todo, pk=task_id)
    task.delete()

    return redirect('/todo/')


def login_page(request):
    if request.method == "POST":

        data = request.POST

        username = data.get('username')
        user_password = data.get('user_password')

        if not User.objects.filter(username = username).exists():
            messages.info(request,"Invaild Username")
            return redirect('/todo/login')

        user = authenticate(username=username, password=user_password)

        if user == None:
            messages.info(request,"Incorrect Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')


    return render(request,"login.html")

def register_page(request):
    if request.method == "POST":

        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        user_password = data.get('user_password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,"Username already taken")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
            )
        

        user.set_password(user_password)
        user.save()
        messages.info(request,"Account created successfully")

        return redirect('/register/')

    return render(request,"register.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def landing_page(request):
    return render(request, "landing_page.html")

