from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'mainpage'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
    path('tasks/<int:pk>/', views.view_task, name='view_task'),
    path('tasks/', views.home, name='home'),
    path('tasks/new', views.create_task, name='new_task'),
    path('tasks/<int:pk>/edit/', views.update_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html')),
]
