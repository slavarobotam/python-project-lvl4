from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from mainpage.models import Status, Task


class TaskForm(forms.ModelForm):
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
        fields = ['username', 'password1', 'password2', ]


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status_value', ]
        labels = {
            'status_value': 'Status name',
        }
