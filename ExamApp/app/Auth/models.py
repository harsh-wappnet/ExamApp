from django.db import models


# Create your models here.
class AppUserTable(models.Model):
    class Meta:
        db_table = "app_user_table"

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    email = models.CharField(blank=True, max_length=50, unique=True)
    user_application_id = models.CharField(blank=False, max_length=12, unique=True)
    user_password = models.CharField(blank=False, max_length=255)
    user_picture = models.ImageField(upload_to="userprofile/")
    first_login = models.BooleanField(blank=False, default=True)
    is_active = models.BooleanField(blank=False, default=False)
    auth_token = models.CharField(blank=False, max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class EmailVerifyTable(models.Model):
    class Meta:
        db_table = "email_verify_table"

    id = models.AutoField(primary_key=True)
    uuid_verification = models.UUIDField(blank=False)
    user = models.ForeignKey(AppUserTable, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uuid_verification
