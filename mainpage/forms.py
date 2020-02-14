from django.forms import ModelForm
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)
