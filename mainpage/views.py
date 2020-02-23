from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from mainpage.forms import SignUpForm, StatusForm, TaskForm
from mainpage.models import Status, Tag, Task


@login_required
def home(request, template_name='home.html'):
    if 'newtask' in request.GET:
        return redirect('/tasks/new')
    if 'mytasks' in request.GET:
        user = request.user
        query_set = Task.objects.filter(assigned_to__username=user)
    if 'reset' in request.GET:
        query_set = Task.objects.all()
    else:
        query_set = query_filter(request)
    context = {
        'queryset': query_set,
        'statuses': Status.objects.all(),
        'tags': Tag.objects.all(),
        'tasks': Task.objects.all(),
        'users': User.objects.all(),
    }
    return render(request, template_name, context)


def is_valid_queryparam(param):
    return param != '' and param is not None


def query_filter(request):
    qs = Task.objects.all()
    tag = request.GET.get('tag')
    status = request.GET.get('status')
    assigned_to = request.GET.get('assigned_to')
    if is_valid_queryparam(status) and status != 'All statuses':
        qs = qs.filter(status__name=status)
    if is_valid_queryparam(tag) and tag != 'All tags':
        qs = qs.filter(tags__name=tag)
    if is_valid_queryparam(assigned_to) and assigned_to != 'Assigned to all':
        qs = qs.filter(assigned_to__username=assigned_to)
    return qs


@login_required
def settings(request, template_name='pages/settings.html'):
    context = {
        'form': StatusForm(),
        'statuses': Status.objects.all(),
    }
    return render(request, template_name, context)


def about(request, template_name='pages/about.html'):
    return render(request, template_name)


def create_status(request, template_name='pages/settings.html'):
    form = StatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/settings/')
    return render(request, template_name, {'form': form})


def delete_status(request, pk, template_name='pages/settings.html'):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('/settings/')
    return render(request, template_name, {'object': status})


def update_status(request, pk, template_name='pages/status_edit.html'):
    status = get_object_or_404(Status, pk=pk)
    form = StatusForm(request.POST or None, instance=status)
    if form.is_valid():
        status = form.save()
        status.save()
        return redirect('/settings/')
    return render(request, template_name, {'form': form})


def view_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    return render(request,
                  'tasks/view_task.html',
                  {'task': task, 'form': form})


def edit_task(request, pk, template_name='tasks/edit_task.html'):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if 'back' in request.POST:
        return redirect('/')
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, template_name, {'form': form, 'task': task})


def create_task(request, template_name='tasks/new_task.html'):
    form = TaskForm(request.POST or None,
                    initial={'name': Task.random_taskname(),
                             'description': '',
                             'creator': request.user,
                             'assigned_to': request.user})
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
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'registration/signup.html', {'form': form})
