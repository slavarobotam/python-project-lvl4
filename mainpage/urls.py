from django.urls import path
from django.views.generic.base import RedirectView

from mainpage import views

app_name = 'mainpage'

urlpatterns = [
    path('', RedirectView.as_view(url='tasks/')),
    path('tasks/', views.Home.as_view(), name='home'),
    path('settings/', views.Settings.as_view(), name='settings'),
    path('about/', views.About.as_view(), name='about'),
    path('statuses/<int:pk>/delete/', views.DeleteStatus.as_view(),
         name='delete_status'),
    path('statuses/new/', views.CreateStatus.as_view(), name='create_status'),
    path('statuses/<int:pk>/edit/', views.UpdateStatus.as_view(),
         name='edit_status'),
    path('tasks/<int:pk>/', views.TaskView.as_view(), name='view_task'),
    path('tasks/new', views.CreateTask.as_view(), name='new_task'),
    path('tasks/<int:pk>/edit/', views.EditTask.as_view(), name='edit_task'),
    path('tasks/<int:pk>/delete/', views.DeleteTask.as_view(),
         name='delete_task'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
