from django.urls import path

from mainpage import views

app_name = 'mainpage'

urlpatterns = [
    path('', views.redirect_to_home),
    path('about/', views.about, name='about'),
    path('settings/', views.settings, name='settings'),
    path('statuses/new/', views.create_status, name='create_status'),
    path('statuses/<int:pk>/edit/', views.update_status, name='edit_status'),
    path('statuses/<int:pk>/delete/', views.delete_status,
         name='delete_status'),
    path('tasks/', views.home, name='home'),
    path('tasks/<int:pk>/', views.view_task, name='view_task'),
    path('tasks/new', views.create_task, name='new_task'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('signup/', views.signup, name='signup'),
]
