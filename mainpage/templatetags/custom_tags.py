from django import template
from ..models import Task
register = template.Library()


@register.simple_tag
def task_lis():
    tasks = Task.objects.all()
    return {'tasks': tasks}
