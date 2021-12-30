from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.utils.html import format_html

from API.models.email_verify import VerifyEmailTable
from API.models.user_profile import UserProfileTable
from API.models.user_token import UserTokenTable


# Register your models here.
class UserTokenDetail(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id', 'user_token', '__user__', 'created_at', 'updated_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserProfileDetail(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id', 'profile_pic', 'user_account_number', 'contact', '__user__', 'created_at', 'updated_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def profile_pic(self, obj):
        if obj.user_profile_image:
            return format_html(
                f'<img src="{settings.BASE_URL}/user_data/{obj.user_profile_image}" alt="" width="40" height="40">')
        return "Not available"

    def contact(self, obj):
        if obj.user_contact:
            return format_html(f'<p>{obj.user_contact}</>')
        return "Not available"


class VerifyEmailDetail(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id', 'uuid_verification', '__user__', 'created_at', 'updated_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# unregister model
admin.site.unregister(Group)
admin.site.unregister(User)

# register model
admin.site.register(UserTokenTable, UserTokenDetail)
admin.site.register(UserProfileTable, UserProfileDetail)
admin.site.register(VerifyEmailTable, VerifyEmailDetail)
