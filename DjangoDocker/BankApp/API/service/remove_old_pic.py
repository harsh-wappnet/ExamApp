import os

from django.conf import settings


def remove_pic(file_name):
    file = settings.MEDIA_ROOT + str(file_name)
    if file_name != "":
        os.remove(file)
