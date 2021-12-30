from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models.user_profile import UserProfileTable
from API.serializer.profile_serializer import ProfileImageSerializer, UserProfileSerializer, UserPasswordSerializer
from API.service.data_base_service import UserData
from API.service.remove_old_pic import remove_pic


class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        db_object = UserData(kwargs['user_id'])
        response = db_object.get_profile()
        return Response(data={"success": True, "user_info": response}, status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):
        serializer_validator = UserProfileSerializer(data=request.data)
        serializer_validator.is_valid(raise_exception=True)

        db_object = UserData(kwargs['user_id'])
        user = db_object.get_user()

        serializer_validator.update(user, serializer_validator.data)
        return Response(data={"success": True, "message": "Profile updated!"}, status=status.HTTP_200_OK)


class UserPasswordView(APIView):
    def patch(self, request, **kwargs):
        serializer_validator = UserPasswordSerializer(data=request.data)
        serializer_validator.is_valid(raise_exception=True)

        db_object = UserData(kwargs['user_id'])
        user = db_object.get_user()

        response = serializer_validator.update(user, serializer_validator.data)
        if response:
            return Response(data={"success": True, "message": "Password updated!"}, status=status.HTTP_200_OK)

        return Response(data={"success": False, "message": "Old password not matched!"},
                        status=status.HTTP_400_BAD_REQUEST)


class UserPicView(APIView):

    def patch(self, request, **kwargs):
        serializer_validator = ProfileImageSerializer(data=request.data)
        serializer_validator.is_valid(raise_exception=True)

        profile = UserProfileTable.objects.get(user=kwargs["user_id"])
        remove_pic(profile.user_profile_image)

        serializer = ProfileImageSerializer(profile, data=request.data, partial=True)

        serializer.is_valid()
        serializer.save()

        return Response(data={"success": True, "message": "Picture updated!"}, status=status.HTTP_200_OK)
