from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'mainpage'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
    path('<int:pk>/', views.view_task, name='view_task'),
    path('new', views.create_task, name='new_task'),
    path('edit/<int:pk>', views.update_task, name='edit_task'),
    path('delete/<int:pk>', views.delete_task, name='delete_task'),
    # path('', views.task_list, name='task_list'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
]
