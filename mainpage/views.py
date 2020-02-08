from django.shortcuts import render, get_object_or_404
from .models import Task


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


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request,
                  'task_details.html',
                  {'task': task})
