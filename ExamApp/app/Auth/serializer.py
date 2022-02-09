import random
import secrets
import uuid
from threading import Thread

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from Auth.models import AppUserTable, EmailVerifyTable


class LoginSerializer(serializers.Serializer):
    user_application_id = serializers.CharField(required=True)
    user_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user_application_id = attrs.get('user_application_id')
        user_password = attrs.get('user_password')

        if AppUserTable.objects.filter(user_application_id=user_application_id).exists():
            user_detail = AppUserTable.objects.get(user_application_id=user_application_id)
            if not user_detail.is_active:
                encrypt_password = check_password(password=user_password, encoded=user_detail.user_password)
                if encrypt_password:
                    return {
                        "status": True,
                        "first_login": user_detail.first_login,
                        "Token": user_detail.auth_token
                    }
                return self.return_response(False, "Invalid credentials!")
            return self.return_response(False, "Account not verified yet!")
        else:
            return self.return_response(False, "Application id is not registered!")

    def return_response(self, status, message):
        return {
            "status": status,
            "message": message
        }


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=AppUserTable.objects.all(), message={"message": "Email already register!"})],
    )

    class Meta:
        model = AppUserTable
        fields = ('first_name', 'last_name', 'email', 'user_picture')

    def create(self, validated_data):
        user_application_id = int("%0.12d" % random.randint(0, 999999999999))
        auth_token = secrets.token_hex()

        user = AppUserTable.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_picture=validated_data['user_picture'],
            user_application_id=user_application_id,
            user_password="",
            auth_token=auth_token
        )

        Thread(target=self.async_send_email, kwargs={"user": user}).start()
        return user

    def async_send_email(self, user):
        unique_verification_code = uuid.uuid4()

        verification = EmailVerifyTable.objects.create(user_id=user.id, uuid_verification=unique_verification_code)
        verification.save()

        subject = "Confirm Your Account"
        message = render_to_string('email_verify.html', {
            'user': user.first_name + " " + user.last_name,
            'verification_code': unique_verification_code,
        })

        email_from = settings.EMAIL_HOST_USER
        return_recipient_list = [
            str(user.email),
        ]

        send_mail(subject, message, email_from, return_recipient_list)
