from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(max_length=150, allow_blank=True, required=False, default='')
    last_name = serializers.CharField(max_length=150, allow_blank=True, required=False, default='')
    is_premium = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = User
        fields = (
            'email', 
            'password', 
            'first_name',
            'last_name',
            'is_premium', 
        )

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_premium=validated_data['is_premium'],
        )
        return user
