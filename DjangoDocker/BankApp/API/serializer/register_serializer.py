import random
import uuid
from threading import Thread

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from API.models.email_verify import VerifyEmailTable
from API.models.user_token import UserTokenTable


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message={"message": "Email already register!"})],
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        username = self.generate_username([validated_data["first_name"], validated_data["last_name"]])
        user = User.objects.create(
            username=username,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()

        self.generate_user_token(user=user)
        Thread(target=self.async_send_email, kwargs={"user": user}).start()

        return user

    def generate_username(self, names):
        first_letter = names[0][0:5]
        three_letters_surname = names[-1][:3]
        number = '{:05d}'.format(random.randrange(1, 999))
        username = (first_letter + three_letters_surname + number)
        return username

    def generate_user_token(self, user):
        UserTokenTable.objects.create(user=user, user_token=uuid.uuid4())

    def async_send_email(self, user):
        unique_verification_code = uuid.uuid4()

        verification = VerifyEmailTable.objects.create(user_id=user.id, uuid_verification=unique_verification_code)
        verification.save()

        subject = "Confirm Your Account"
        message = render_to_string('verify_email.html', {
            'user': user.email,
            'verification_code': unique_verification_code,
        })

        email_from = settings.EMAIL_HOST_USER
        return_recipient_list = [
            str(user.email),
        ]

        send_mail(subject, message, email_from, return_recipient_list)
