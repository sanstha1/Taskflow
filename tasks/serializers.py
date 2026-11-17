from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'is_completed',
            'created_at',
            'updated_at'
        ]

        read_only_fields=[
            'id',
            'created_at',
            'updated_at'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user