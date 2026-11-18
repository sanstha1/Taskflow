
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError


from .models import Task
from .serializers import TaskSerializer , UserRegistrationSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):

    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)

    elif request.method == 'PATCH':
        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):

    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {
                'message':'User Registered Successfully!',
                'username' : user.username,
                'email' : user.email
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):

    try:
        refresh_token = request.data.get('refresh')

        token = RefreshToken(refresh_token)

        token_user_id = token.get(api_settings.USER_ID_CLAIM)

        if str(token_user_id) != str(request.user.pk):
            return Response(
                {
                    'error':'You cannot blacklist another user\'s token.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        token.blacklist()

        return Response(
            {
                'message':'Logged Out Successfully.'
            },
            status=status.HTTP_205_RESET_CONTENT
        )

    except (TokenError,KeyError,TypeError):
        return Response(
            {
                'error':'Invalid Refresh Token.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    