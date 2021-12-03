from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'real_name',
            'gender',
            'stuID'
        ]
        read_only_fields = ['user']

    def create(self,validated_data):
        user = self.context.get('request').user
        userprofile = UserProfile.objects.create(user = user,real_name = validated_data['real_name'],gender = validated_data['gender'],stuID = validated_data['stuID'])
        return userprofile