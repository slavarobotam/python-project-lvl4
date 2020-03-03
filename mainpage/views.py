from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from mainpage.forms import SignUpForm, StatusForm, TaskForm
from mainpage.models import Status, Tag, Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.views.generic.base import TemplateView


class Home(ListView, LoginRequiredMixin):
    template_name = 'home.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.GET.get('newtask'):
            return redirect('/tasks/new')
        query_set = query_filter(self.request)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'queryset': self.get_queryset(),
            'statuses': Status.objects.all(),
            'tags': Tag.objects.all(),
            'tasks': Task.objects.all(),
            'users': User.objects.all(),
            })
        return context


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
    if 'mytasks' in request.GET:
        user = request.user
        qs = Task.objects.filter(assigned_to__username=user)
    if 'reset' in request.GET:
        qs = Task.objects.all()
    return qs


class Settings(ListView, LoginRequiredMixin):
    template_name = 'pages/settings.html'
    model = Status
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': StatusForm(),
            'statuses': Status.objects.all(),
            })
        return context


class About(TemplateView):
    template_name = "pages/about.html"


class CreateStatus(CreateView):
    template_name = 'pages/settings.html'
    model = Status
    success_url = reverse_lazy('mainpage:settings')
    form_class = StatusForm

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteStatus(DeleteView):
    template_name = 'pages/settings.html'
    model = Status
    success_url = reverse_lazy('mainpage:settings')


class UpdateStatus(UpdateView):
    template_name = 'pages/status_edit.html'
    model = Status
    success_url = reverse_lazy('mainpage:settings')
    fields = ['name']

    def form_valid(self, form):
        return super().form_valid(form)


def view_task(request, pk, template_name='tasks/view_task.html'):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST or None, instance=task)
        return render(request,
                      template_name,
                      {'task': task, 'form': form})
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request,
                      template_name,
                      {'task': task, 'form': form})
    else:
        return HttpResponseBadRequest('Bad request')


def edit_task(request, pk, template_name='tasks/edit_task.html'):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, template_name, {'form': form, 'task': task})
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, template_name, {'form': form, 'task': task})
    else:
        return HttpResponseBadRequest('Bad request')


def create_task(request, template_name='tasks/new_task.html'):
    if request.method == 'POST':
        form = TaskForm(request.POST or None,
                        initial={'name': Task.random_taskname(),
                                 'description': '',
                                 'creator': request.user,
                                 'assigned_to': request.user})
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, template_name, {'form': form})
    if request.method == 'GET':
        form = TaskForm(request.GET or None,
                        initial={'name': Task.random_taskname(),
                                 'description': '',
                                 'creator': request.user,
                                 'assigned_to': request.user})
        return render(request, template_name, {'form': form})
    else:
        return HttpResponseBadRequest('Bad request')


def delete_task(request, pk, template_name='tasks/task_confirm_delete.html'):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=pk)
        return render(request, template_name, {'object': task})
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('/')
    else:
        return HttpResponseBadRequest('Bad request')


def signup(request):
    if request.method == 'GET':
        form = SignUpForm(request.GET or None)
        return render(request, 'registration/signup.html', {'form': form})
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return HttpResponseBadRequest('Bad request')
