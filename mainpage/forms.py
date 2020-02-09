from django.forms import ModelForm
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name',
                  'description',
                  'status',
                  'creator',
                  'assigned_to',
                  'tags']
        labels = {
            'name': 'Task name',
            'description': 'Task details',
            'status': 'Status',
            'creator': 'Creator',
            'assigned_to': 'Assigned',
        }
