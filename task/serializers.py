from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class TaskSerializer(serializers.ModelSerializer):
    isDone = serializers.SerializerMethodField(read_only=True)
    if isDone:
        class Meta:
            model = Task
            fields = ['id', 'user', 'header', 'description', 'isDone', 'doneAt']
    
    else:
        class Meta:
            model = Task
            fields = ['id', 'user', 'header', 'description', 'deadline', 'isDone', 'isOverDued']

    def get_isDone(self, obj):
        if obj.isDone:
            return True
        else:
            return False

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin']

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
    
    def get__id(self, obj):
        return obj.id
    
    def get_isAdmin(self, obj):
        return obj.is_staff
    
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)