from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class UserProfileTable(models.Model):
    class Meta:
        db_table = "user_profile_table"

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered "
                                         "in the format: '+999999999'. Up to 10 digits allowed.")

    id = models.AutoField(primary_key=True)
    user_profile_image = models.ImageField(upload_to="userprofile/")
    user_account_number = models.BigIntegerField(blank=False, unique=True)
    user_contact = models.CharField(max_length=10, blank=False, validators=[phone_regex])
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __info__(self):
        return {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'user_account_number': self.user_account_number,
            'user_contact': self.user_contact or None,
            'user_profile_image': f"{settings.BASE_URL}" + self.user_profile_image.url if self.user_profile_image else None
        }

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def __user__(self):
        return self.user.first_name + " " + self.user.last_name
