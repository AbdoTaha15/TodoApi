from django.utils import timezone
from task.serializers import *
from task.models import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTask(request, pk):
    user = request.user
    task = user.task_set.get(pk=pk)
    isOverDued(task)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTasks(request):
    user = request.user
    tasks = user.task_set.all().order_by('id')

    if not tasks:
        return Response({'detail':'No available tasks'})

    else:
        # if a task has a deadline, check if it's overdued
        for task in tasks:
            isOverDued(task)

        page = request.query_params.get('page')
        
        paginator = Paginator(tasks, 5)

        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        
        if page == None:
            page = 1
        
        page = int(page)

        serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks':serializer.data, 'page':page, 'pages': paginator.num_pages})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTask(request):
    user = request.user

    data = request.data

    task = Task.objects.create(
        user=user,
        header = data['header'],
        description = data['description'],
        deadline = data['deadline'],
    )

    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateTask(request, pk):
    user = request.user
    task = user.task_set.get(pk=pk)
    data = request.data
    isOverDued(task)

    task.header = data['header']
    task.description = data['description']

    if 'deadline' in data.keys():
        oldDeadline = task.deadline
        task.deadline = data['deadline']
        if task.deadline < oldDeadline:
            return Response({'detail':'Can\'t update deadline'}, status=status.HTTP_400_BAD_REQUEST)
    
    task.save()
    serializer = TaskSerializer(task, many=False)
    return Response({'task':serializer.data, 'detail':'Task updated'}, status=status.HTTP_200_OK)

def updateDeadline(task, data):

    oldDeadline = task.deadline
    
    task.deadline = data['deadline']

    if task.deadline < oldDeadline:
        return Response({'detail':'Can\'t update deadline'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return task.deadline

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTask(request, pk):
    user = request.user
    task = user.task_set.get(pk=pk)
    task.delete()
    return Response({'detail': 'Task is successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

def isOverDued(task):
    # if a task has a deadline, check if it's overdued
    if task.deadline:
        d = timezone.now()
        if task.deadline < d:
            task.isOverDued = True

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateTaskToDone(request, pk):
    user = request.user
    task = user.task_set.get(pk=pk)
    task.isDone = True
    task.doneAt = timezone.now()
    task.save()
    return Response('Task is done.')