# Create your views here.
import secrets
from threading import Thread

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from Auth.models import AppUserTable, EmailVerifyTable
from Auth.serializer import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = AppUserTable.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={
            'status': True,
            'message': 'Register successfully, please check your email and verify your account!',
        }, status=status.HTTP_200_OK)


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.validate(request.data)
        return Response(data=response, status=status.HTTP_200_OK if response['status'] else status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):

    def get(self, request, verification_code):
        verification_object = EmailVerifyTable.objects.filter(uuid_verification=verification_code)
        if verification_object.count() > 0:

            user_instance = AppUserTable.objects.get(id=verification_object[0].user_id)
            AppUserTable.objects.filter(id=user_instance.id).update(is_active=True)
            verify_object = EmailVerifyTable.objects.get(user_id=user_instance.id,
                                                         uuid_verification=verification_code)
            verify_object.delete()

            user_password = secrets.token_hex(7)
            encrypt_password = make_password(user_password)
            user_instance.user_password = encrypt_password
            user_instance.save()

            Thread(target=self.async_send_email,
                   kwargs={'user': user_instance, 'one_time_password': user_password}).start()

            return Response(
                data={
                    "status": True,
                    "message": "Email verified successfully! Please check your inbox for your Application id and "
                               "password "
                },
                status=status.HTTP_200_OK)
        else:
            return Response(
                data={"status": False, "message": f"Email is either verified or not valid or expired!"},
                status=status.HTTP_400_BAD_REQUEST)

    def async_send_email(self, user, one_time_password):
        subject = "Account verified!"
        message = render_to_string('account_verified.html', {
            'user': user.first_name + " " + user.last_name,
            'application_id': user.user_application_id,
            'password': one_time_password
        })

        email_from = settings.EMAIL_HOST_USER
        return_recipient_list = [
            str(user.email),
        ]

        send_mail(subject, message, email_from, return_recipient_list)
