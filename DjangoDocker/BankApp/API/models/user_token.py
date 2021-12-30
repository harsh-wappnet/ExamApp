from django.contrib.auth.models import User
from django.db import models


class UserTokenTable(models.Model):
    class Meta:
        db_table = "user_token_table"

    id = models.AutoField(primary_key=True)
    user_token = models.UUIDField(blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def __user__(self):
        return self.user.first_name + " " + self.user.last_name