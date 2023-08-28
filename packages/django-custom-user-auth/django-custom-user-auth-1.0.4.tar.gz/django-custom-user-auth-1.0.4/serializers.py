from rest_framework import serializers
from user_service.user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password']

    def create(self, validated_data) -> CustomUser:
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data) -> CustomUser:
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)