from django.urls import path
from task.views import task_views 
urlpatterns = [
    path('', task_views.getTasks, name='user-tasks'),
    path('create/', task_views.createTask, name='create-task'),
    path('<str:pk>/', task_views.getTask, name='user-task'),
    path('<str:pk>/done/', task_views.updateTaskToDone, name='task-is-done'),
    path('<str:pk>/update/', task_views.updateTask, name='update-task'),
    path('<str:pk>/delete/', task_views.deleteTask, name='delete-task'),
]