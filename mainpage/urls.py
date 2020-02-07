from django.urls import path

from . import views


urlpatterns = [

]


app_name = 'mainpage'

urlpatterns = [
    path('index/', views.index, name='index'),
    # task views
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_detail, name='task_details'),
]
