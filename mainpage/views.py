from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render

from mainpage.forms import SignUpForm, StatusForm, TaskForm
from mainpage.models import Status, Tag, Task
from django.contrib.auth.models import User


def home(request, template_name='tasks/home.html'):
    query_set = query_filter(request)
    next = request.POST.get('next', '/')
    context = {
        'queryset': query_set,
        'statuses': Status.objects.all(),
        'tags': Tag.objects.all(),
        'tasks': Task.objects.all(),
        'users': User.objects.all(),
        'next': next
    }
    if 'newtask' in request.GET:
        return redirect('/tasks/new')
    return render(request, template_name, context)


def is_valid_queryparam(param):
    return param != '' and param is not None


def query_filter(request):
    qs = Task.objects.all()
    tag = request.GET.get('tag')
    status = request.GET.get('status')
    assigned_to = request.GET.get('assigned_to')
    if 'mytasks' in request.GET:
        user = request.user
        qs = qs.filter(assigned_to__username=user)
    if 'reset' in request.GET:
        qs = Task.objects.all()
    if is_valid_queryparam(status) and status != 'Status':
        qs = qs.filter(status__status_value=status)
    if is_valid_queryparam(tag) and tag != 'Tag':
        qs = qs.filter(tags__name=tag)
    if is_valid_queryparam(assigned_to) and assigned_to != 'Assigned to':
        qs = qs.filter(assigned_to__username=assigned_to)
    return qs


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
                  'view_task.html',
                  {'task': task, 'form': form})


def update_task(request, pk, template_name='tasks/task_form.html'):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return render(request, 'view_task.html', {'task': task, 'form': form})
    return render(request, template_name, {'form': form, 'task': task})


def create_task(request, template_name='tasks/new_task.html'):
    form = TaskForm(request.POST or None,
                    initial={'name': Task.random_taskname(),
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
