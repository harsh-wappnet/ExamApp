import uuid
from threading import Thread

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models.reset_password import ResetPasswordTable
from API.serializer.forget_password_serializer import ForgetPasswordSerializer
from API.service.data_base_service import DBMethods


class ForgetPasswordView(APIView):
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_service_object = DBMethods(email=request.data['email'])
        if db_service_object.is_exist():
            user = db_service_object.get_user()
            Thread(target=self.async_send_email, kwargs={'user': user}).start()
            return Response(
                data={
                    "status": True,
                    "message": "Reset password link send to email Id!"
                },
                status=status.HTTP_200_OK)

        return Response(
            data={
                "status": False,
                "message": "Email id not register!"
            },
            status=status.HTTP_400_BAD_REQUEST)

    def async_send_email(self, user):
        unique_verification_code = uuid.uuid4()

        ResetPasswordTable.objects.filter(user_id=user.id).delete()
        reset_request = ResetPasswordTable.objects.create(user_id=user.id, uuid_verification=unique_verification_code)
        reset_request.save()

        user_name = user.first_name + " " + user.last_name
        subject = "Forget Password!"

        message = render_to_string('forget_password.html', {
            'user': user_name,
            'token': unique_verification_code,
        })

        email_from = settings.EMAIL_HOST_USER
        return_recipient_list = [
            str(user.email),
        ]

        send_mail(subject, message, email_from, return_recipient_list)


def reset_password_view(request, verification_code):
    if request.method == "GET":
        code_verification = ResetPasswordTable.objects.filter(uuid_verification=verification_code)
        if code_verification.count() > 0:
            verify_request_object = ResetPasswordTable.objects.filter(user_id=code_verification[0].user_id,
                                                                      uuid_verification=verification_code)
            if verify_request_object.count() > 0:
                return render(request, 'reset_password.html', {'uuid': verification_code, 'message': None})
        else:
            return render(request, 'reset_password.html', {'uuid': None, 'message': None})


def update_password_view(request):
    if request.method == "POST":
        request_verification = ResetPasswordTable.objects.filter(uuid_verification=request.POST['uuid'])

        if request_verification.count() > 0:
            password = request.POST['new_pass']
            new_password = request.POST['confirm_new_pass']

            if password == new_password:
                enc_pass = make_password(request.POST['new_pass'])
                psw = User.objects.get(id=request_verification[0].user_id)
                psw.password = enc_pass
                psw.save()
                ResetPasswordTable.objects.filter(user_id=request_verification[0].user_id).delete()
                return render(request, 'reset_password.html',
                              {'uuid': None, 'message': 'Password Updated Successfully!'})
            else:
                return render(request, 'reset_password.html',
                              {'uuid': request.POST['uuid'], 'message': 'Password and confirm password not matched!'})
        else:
            return render(request, 'reset_password.html',
                          {'uuid': None, 'message': 'Request expired'})
