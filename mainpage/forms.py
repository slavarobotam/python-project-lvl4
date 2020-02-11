from django.forms import ModelForm
from .models import Task
from django.forms.forms import BaseForm
from django import forms
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
    # first_name = forms.CharField(max_length=100, help_text='Last Name')
    # last_name = forms.CharField(max_length=100, help_text='Last Name')
    # email = forms.EmailField(max_length=150, help_text='Email')


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)
        # fields = ('username', 'first_name', 'last_name',
        #           'email', 'password1', 'password2',)