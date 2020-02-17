import django_filters

from mainpage.models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['creator',
                  'status__status_value',
                  'assigned_to',
                  'tags__name']
