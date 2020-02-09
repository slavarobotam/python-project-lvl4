from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from .models import Task


def contact(request):
    return render(request, 'pages/contact.html')


def features(request):
    return render(request, 'pages/features.html')


def task_list(request):
    tasks = Task.objects.all()
    return render(request,
                  'task_list.html',
                  {'tasks': tasks})


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
