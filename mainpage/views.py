from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django_filters.views import FilterView

from mainpage.filters import TaskFilter
from mainpage.forms import SignUpForm, StatusForm, TaskForm
from mainpage.models import Status, Tag, Task
from django.contrib.auth.models import User

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



def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Task.objects.all()

    tag = request.GET.get('tag')
    status = request.GET.get('status')
    assigned_to = request.GET.get('assigned_to')

    if 'mytasks' in request.GET:
        user = request.user
        qs = qs.filter(assigned_to__username=user)
        
    if is_valid_queryparam(status) and status != 'Choose...':
        qs = qs.filter(status__status_value=status)

    if is_valid_queryparam(tag) and tag != 'Choose...':
        qs = qs.filter(tags__name=tag)

    if is_valid_queryparam(assigned_to) and assigned_to != 'Choose...':
        qs = qs.filter(assigned_to__username=assigned_to)
    return qs

def FilterView(request):
    qs = filter(request)
    context = {
        'queryset': qs,
        'statuses': Status.objects.all(),
        'tags': Tag.objects.all(),
        'tasks': Task.objects.all(),
        'users': User.objects.all()
    }
    return render(request, "tasks/djtasks.html", context)


def task_list(request):
    tasks = Task.objects.all()
    users = User.objects.all()
    statuses = Status.objects.all()
    if request.method == 'GET' and 'mytasks' in request.GET:
        user = request.user
        
        f = TaskFilter(request.GET, queryset=Task.objects.filter(assigned_to=user))
        return render(request, 'task_list.html', {'filter': f, 'tasks': tasks, 'users': users, 'statuses': statuses})
    f = TaskFilter(request.GET, queryset=Task.objects.all())
    return render(request, 'task_list.html', {'filter': f,
                                              'tasks': tasks,
                                              'users': users, 'statuses': statuses})


def sort_btn(request):
    user = request.user
    f = TaskFilter(request.GET, queryset=Task.objects.filter(assigned_to=user))
    return render(request, 'task_list.html', {'filter': f})

# class TaskList(FilterView):
#     model = Task
#     filter_class = TaskFilter
#     context_object_name = 'tasks'
#     filter_class = TaskFilter
#     template_name = 'task_list.html'
    # def get_context_data(self, **kwargs):
    #     context = super(MyPost, self).get_context_data(**kwargs)
    #     context['post'] = Post.objects.filter(live=True, user=self.request.user)  # used self for object reference
    #     return context

# def BootstrapFilterView(request):
#     qs = filter(request)
#     context = {
#         'queryset': qs,
#         'tags': Tag.objects.all(),
#         'statuses': Status.objects.all(),
#     }
#     return render(request, 'home.html', context)


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
                             'assigned_to': user,
                             'status': 1})
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, template_name, {'form': form})


def update_task(request, pk, template_name='tasks/task_form.html'):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
        'statuses': Status.objects.all(),
        'tags': Tag.objects.all(),
        'tasks': Task.objects.all(),
        'users': User.objects.all()
    }
    return render(request, template_name, context)


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
