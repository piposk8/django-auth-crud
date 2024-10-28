from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from.models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html')

# Función para agregar usuarios
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Error en el registro, verifica los datos.'
            })
            
@login_required
def tasks(request):
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks':tasks})
@login_required
def tasks_completed(request):
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ('-datecompleted')
    return render(request, 'tasks.html',{'tasks':tasks})

#Crear TArea
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': TaskForm
        })
    else:
        try:
            form=TaskForm(request.POST)
            new_task=form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'escribe datos validos'
        })
        
@login_required        
def task_detail(request,task_id):
    if request.method == 'GET':
        task=get_object_or_404(Task, pk=task_id, user = request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form': form})
    else:
        try:
            task=get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task,
            'form': form, 'error': "No se puedo actualizar"})

@login_required            
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk = task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')
@login_required    
def delete_task(request,task_id):
    task = get_object_or_404(Task, pk = task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required        
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signin.html', {
                'form': form,
                'error': 'El usuario o contraseña son incorrectos.'
            })


#1.35.32
#1.53.06
#2.17.00
#2.37.39
