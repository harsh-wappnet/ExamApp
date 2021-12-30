from django.contrib.auth.models import User

from API.models.user_profile import UserProfileTable


class UserData:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_profile(self):
        user_data = UserProfileTable.objects.get(user=self.user_id)
        return user_data.__info__()

    def get_user(self):
        return User.objects.get(id=self.user_id)


class DBMethods:
    def __init__(self, email):
        self.email = email

    def is_exist(self):
        return User.objects.filter(email=self.email).exists()

    def get_user(self):
        return User.objects.get(email=self.email)
