from django.contrib.auth.models import User
from rest_framework import serializers


class ForgetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)
