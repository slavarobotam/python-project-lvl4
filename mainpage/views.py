from django.shortcuts import render, get_object_or_404, redirect
from mainpage.forms import TaskForm, SignUpForm, StatusForm
from mainpage.models import Task, Status
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


def contact(request):
    return render(request, 'pages/contact.html')


def statuses(request):
    statuses = Status.objects.all()
    form = StatusForm()
    return render(request, 'pages/statuses.html', {'statuses': statuses, 'form': form})


def create_status(request):
    form = StatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/statuses/')
    return render(request, 'pages/statuses.html', {'form': form})


def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('/statuses/')
    return render(request, 'pages/statuses.html', {'object': status})


@login_required(login_url='/accounts/login/')
def home(request):
    tasks = Task.objects.all()
    return render(request, 'home.html', {'tasks': tasks})


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
    if request.method == 'DELETE':
        task.delete()
        return redirect('/')
    return render(request, template_name, {'object': task})


def signup(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'registration/signup.html', {'form': form})
