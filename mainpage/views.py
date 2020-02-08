from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskForm


def index(request):
    return render(request, 'index.html')


def main(request):
    return render(request, 'main.html')


def contact(request):
    return render(request, 'contact.html')


def features(request):
    return render(request, 'features.html')


def task_list(request):
    tasks = Task.objects.all()
    return render(request,
                  'task_list.html',
                  {'tasks': tasks})


def task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request,
                  'task_view.html',
                  {'task': task})


def task_create(request, template_name='tasks/task_form.html'):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, template_name, {'form': form})


def task_update(request, pk, template_name='tasks/task_form.html'):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, template_name, {'form': form})


def task_delete(request, pk, template_name='tasks/task_confirm_delete.html'):
    task = get_object_or_404(Task, pk=pk)    
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, template_name, {'object': task})
