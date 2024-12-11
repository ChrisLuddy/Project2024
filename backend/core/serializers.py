# core/serializers.py
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        role = validated_data['role']
        if role == 'fund_admin':
            group = Group.objects.get(name='FundAdmin')
        elif role == 'fund_manager':
            group = Group.objects.get(name='FundManager')
        else:
            group = None
        
        if group:
            user.groups.add(group)

        return user
