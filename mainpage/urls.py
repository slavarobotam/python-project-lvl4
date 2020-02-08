from django.urls import path

from . import views

app_name = 'mainpage'

urlpatterns = [
    path('index/', views.index, name='index'),
    # task views
    path('main/', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_view, name='task_view'),
    path('new', views.task_create, name='task_new'),
    path('edit/<int:pk>', views.task_update, name='task_edit'),
    path('delete/<int:pk>', views.task_delete, name='task_delete'),

]
