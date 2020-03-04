from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)
from django.views.generic.base import TemplateView

from mainpage.forms import SignUpForm, StatusForm, TaskForm
from mainpage.models import Status, Tag, Task


class Home(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'home.html'
    model = Task
    context_object_name = 'tasks'

    @staticmethod
    def add_filter(filters, lookup, query, if_not=None):
        if query and query != if_not:
            filters[lookup] = query

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET.get('tag')
        status = self.request.GET.get('status')
        assigned_to = self.request.GET.get('assigned_to')
        filters = {}
        self.add_filter(filters, 'status__name', status, if_not='All statuses')
        self.add_filter(filters, 'tags__name', tag, if_not='All tags')
        self.add_filter(filters, 'assigned_to__username', assigned_to,
                        if_not='Assigned to all')
        if 'mytasks' in self.request.GET:
            self.add_filter(filters, 'assigned_to__username',
                            self.request.user)
        if 'reset' in self.request.GET:
            filters = {}
        qs = qs.filter(**filters)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'queryset': self.get_queryset(),
            'statuses': Status.objects.all(),
            'tags': Tag.objects.all(),
            'users': User.objects.all(),
            })
        return context


class Settings(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
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


class DeleteStatus(DeleteView):
    template_name = 'pages/settings.html'
    model = Status
    success_url = reverse_lazy('mainpage:settings')


class UpdateStatus(UpdateView):
    template_name = 'pages/status_edit.html'
    model = Status
    success_url = reverse_lazy('mainpage:settings')
    fields = ['name']


class TaskView(DetailView):
    template_name = 'tasks/view_task.html'
    model = Task


class CreateTask(CreateView):
    template_name = 'tasks/new_task.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('mainpage:home')

    def get_initial(self):
        initial = super(CreateTask, self).get_initial()
        initial['name'] = Task.random_taskname()
        initial['creator'] = self.request.user
        initial['assigned_to'] = self.request.user
        initial['description'] = 'Things to do:'
        return initial


class EditTask(UpdateView):
    template_name = 'tasks/edit_task.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('mainpage:home')


class DeleteTask(DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('mainpage:home')


class SignUp(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('mainpage:home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)
