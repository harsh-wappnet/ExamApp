import random
from threading import Thread

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models.email_verify import VerifyEmailTable
from API.models.user_profile import UserProfileTable
from API.models.user_token import UserTokenTable
from API.serializer.login_serializer import LoginUserSerializer
from API.serializer.register_serializer import RegisterSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_token = UserTokenTable.objects.get(user=user).user_token
        return Response(data={"status": True, "Token": f"{user_token}"}, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={
            'status': True,
            'message': 'Register successfully, please check your email and verify your account!',
        })


class VerifyEmailView(APIView):

    def get(self, request, verification_code):
        verification_object = VerifyEmailTable.objects.filter(uuid_verification=verification_code)
        if verification_object.count() > 0:

            user_instance = User.objects.get(id=verification_object[0].user_id)
            account_number = int("%0.12d" % random.randint(0, 999999999999))

            verify_object = VerifyEmailTable.objects.get(user_id=user_instance.id,
                                                         uuid_verification=verification_code)

            User.objects.filter(id=user_instance.id).update(is_active=True)
            verify_object.delete()

            UserProfileTable.objects.create(user=user_instance, user_account_number=account_number,
                                            user_contact="").save()
            Thread(target=self.async_send_email,
                   kwargs={'email': user_instance.email, 'account_number': account_number}).start()

            return Response(
                data={
                    "status": True,
                    "message": "Email verified successfully! Please check your inbox for your Account number"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(
                data={"status": False, "message": f"Email is either verified or not valid or expired!"},
                status=status.HTTP_400_BAD_REQUEST)

    def async_send_email(self, email, account_number):
        subject = "Account verified!"
        message = render_to_string('account_verified.html', {
            'user': email,
            'account_number': account_number,
        })

        email_from = settings.EMAIL_HOST_USER
        return_recipient_list = [
            str(email),
        ]

        send_mail(subject, message, email_from, return_recipient_list)
