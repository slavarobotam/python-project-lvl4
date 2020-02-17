from django.contrib.auth import views as auth_views
from django.urls import include, path

from mainpage.views import TaskList

from . import views

app_name = 'mainpage'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('settings/', views.settings, name='settings'),
    path('statuses/<int:pk>/delete/',
         views.delete_status,
         name='delete_status'),
    path('statuses/new/', views.create_status, name='create_status'),
    path('statuses/<int:pk>/edit/', views.update_status, name='edit_status'),
    path('tasks/<int:pk>/', views.view_task, name='view_task'),
    path('tasks/new', views.create_task, name='new_task'),
    path('tasks/<int:pk>/edit/', views.update_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('', TaskList.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html')),
]
