from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from API.models.user_profile import UserProfileTable


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileTable
        fields = ('user_profile_image',)


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = UserProfileTable
        fields = ('user_contact', 'first_name', 'last_name')

    def update(self, user, validated_data):
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        UserProfileTable.objects.filter(user_id=user.id).update(user_contact=validated_data.get('user_contact'))
        user.save()
        return user


class UserPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'new_password')

    def update(self, user, validated_data):
        validate = user.check_password(validated_data.get('password'))
        if validate:
            user.set_password(validated_data.get('new_password'))
            user.save()
            return True
        return False
