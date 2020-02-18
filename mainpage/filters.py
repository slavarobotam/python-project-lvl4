import django_filters
from django import forms
from mainpage.models import Task, Status, Tag
from django.contrib.auth.models import User


def user_tasks(request):
    if request is None:
        return Task.objects.none()
    return Task.objects.filter(assigned_to=request.user)
    # return user.task_set.all()


def assigned_task(request):
    if request is None:
        return Task.objects.none()
    assigned_to = request.GET.get('assigned_to')
    return Task.objects.filter(assigned_to=assigned_to)


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(empty_label='All statuses', field_name='status', queryset=Status.objects.all())
    # my_tasks = django_filters.BooleanFilter(
    #     label="Мои задачи",
    #     method='my_task_filter',
    #     widget=forms.CheckboxInput()
    # )
    tas = django_filters.ModelChoiceFilter(
        # name='tas',
        lookup_expr='isnull',
        empty_label='All tasks',
        queryset=Task.objects.all(),
        method='filter_assigned',
    )
    assigned_to = django_filters.ModelChoiceFilter(empty_label='All users', field_name='assigned_to', queryset=User.objects.all())
    tags = django_filters.ModelChoiceFilter(empty_label='All tags', queryset=Tag.objects.all())

    # userr = django_filters.ModelChoiceFilter(
    #     field_name='userr', lookup_expr='isnull',
    #     empty_label='All assigned_to',
    #     queryset=user_tasks,
    # )
    class Meta:
        model = Task
        fields = [
                  'status',
                #   'userr',
                #   'assigned_to',
                #   'tags',
                #   'tags__name',
                  ]

    # def filter_assigned(self, queryset, name, value):
    #     return queryset.filter(assigned_to=self.request.user)

    
