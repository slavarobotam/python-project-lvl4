from django import forms
from mainpage.models import Task, Status
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
        fields = ['username', 'password1', 'password2',]


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status_value', ]
