from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django_filters.views import FilterView

from mainpage.filters import TaskFilter
from mainpage.forms import SignUpForm, StatusForm, TaskForm
from mainpage.models import Status, Tag, Task


def contact(request):
    return render(request, 'pages/contact.html')


def settings(request):
    statuses = Status.objects.all()
    form = StatusForm()
    return render(request,
                  'pages/settings.html',
                  {'statuses': statuses, 'form': form})


def create_status(request):
    form = StatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/settings/')
    return render(request, 'pages/settings.html', {'form': form})


def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('/settings/')
    return render(request, 'pages/settings.html', {'object': status})


def update_status(request, pk, template_name='pages/status_edit.html'):
    status = get_object_or_404(Status, pk=pk)
    form = StatusForm(request.POST or None, instance=status)
    if form.is_valid():
        status = form.save()
        status.save()
        messages.success(request, "You successfully updated the status")
        return redirect('/settings/')
    return render(request, template_name, {'form': form})


class TaskList(FilterView):
    model = Task
    filter_class = TaskFilter
    context_object_name = 'tasks'
    filter_class = TaskFilter
    template_name = 'task_list.html'


def BootstrapFilterView(request):
    qs = filter(request)
    context = {
        'queryset': qs,
        'tags': Tag.objects.all(),
        'statuses': Status.objects.all(),
    }
    return render(request, 'home.html', context)


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
