from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            if User.objects.filter(email=email).exists():
                user_detail = User.objects.get(email=email)

                user = authenticate(request=self.context.get('request'),
                                    username=user_detail.username, password=password)

                if not user_detail.is_active:
                    message = {
                        'info': {'status': False, 'message': 'Email not verified yet!'}
                    }
                    raise serializers.ValidationError(message)
            else:
                message = {"info": {'status': False, 'message': 'Email id is not registered.'}}
                raise serializers.ValidationError(message)

            if not user:
                message = {
                    'info': {'status': False, 'message': 'Unable to log in with provided credentials.'}
                }
                raise serializers.ValidationError(message, code='authorization')

            attrs['user'] = user
        return attrs
