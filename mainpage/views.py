from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect

from mainpage.forms import SignUpForm, StatusForm, TaskForm
from mainpage.models import Status, Tag, Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
    FormView
)
from django.views.generic.base import TemplateView


class Home(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'home.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        qs = Task.objects.all()
        tag = self.request.GET.get('tag')
        status = self.request.GET.get('status')
        assigned_to = self.request.GET.get('assigned_to')
        if is_valid_query(status) and status != 'All statuses':
            qs = qs.filter(status__name=status)
        if is_valid_query(tag) and tag != 'All tags':
            qs = qs.filter(tags__name=tag)
        if is_valid_query(assigned_to) and assigned_to != 'Assigned to all':
            qs = qs.filter(assigned_to__username=assigned_to)
        if 'mytasks' in self.request.GET:
            user = self.request.user
            qs = Task.objects.filter(assigned_to__username=user)
        if 'reset' in self.request.GET:
            qs = Task.objects.all()
        return qs

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


def is_valid_query(param):
    return param != '' and param is not None


def query_filter(request):
    qs = Task.objects.all()
    tag = request.GET.get('tag')
    status = request.GET.get('status')
    assigned_to = request.GET.get('assigned_to')
    if is_valid_query(status) and status != 'All statuses':
        qs = qs.filter(status__name=status)
    if is_valid_query(tag) and tag != 'All tags':
        qs = qs.filter(tags__name=tag)
    if is_valid_query(assigned_to) and assigned_to != 'Assigned to all':
        qs = qs.filter(assigned_to__username=assigned_to)
    if 'mytasks' in request.GET:
        user = request.user
        qs = Task.objects.filter(assigned_to__username=user)
    if 'reset' in request.GET:
        qs = Task.objects.all()
    return qs


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
