from django.urls import path
from mainpage import views
from django.views.generic.base import RedirectView

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

    path('tasks/<int:pk>/', views.view_task, name='view_task'),
    path('tasks/new', views.create_task, name='new_task'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('signup/', views.signup, name='signup'),
]
