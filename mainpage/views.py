from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from .models import Task
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required



def contact(request):
    return render(request, 'pages/contact.html')


def features(request):
    return render(request, 'pages/features.html')


@login_required(login_url='/accounts/login/')
def home(request):
    tasks = Task.objects.all()
    return render(request, 'home.html', {'tasks': tasks})



# def task_list(request):
#     tasks = Task.objects.all()
#     return render(request,
#                   'task_list.html',
#                   {'tasks': tasks})


def view_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request,
                  'view_task.html',
                  {'task': task})


def create_task(request, template_name='tasks/task_form.html'):
    user = request.user
    form = TaskForm(request.POST or None,
                    initial={'name': 'Task',
                             'creator': user,
                             'assigned_to': user})
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, template_name, {'form': form})


def update_task(request, pk, template_name='tasks/task_form.html'):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, template_name, {'form': form})


def delete_task(request, pk, template_name='tasks/task_confirm_delete.html'):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, template_name, {'object': task})


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'registration/signup.html', {'form': form})


    