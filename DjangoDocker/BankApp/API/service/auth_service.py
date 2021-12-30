from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from API.models.user_token import UserTokenTable


class AuthMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        view_name = '.'.join((view_func.__module__, view_func.__name__))

        # If the view name is in our exclusion list, exit early
        exclusion_set = getattr(settings, 'EXCLUDE_FROM_MY_MIDDLEWARE', set())

        if request.path.startswith(reverse('admin:index')) or request.path.startswith('/user_data/'):
            return None

        if view_name in exclusion_set:
            return None

        try:

            if "Authorization" not in request.headers.keys():
                response = Response(
                    data={"message": f"Authorization token missing"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response

            if UserTokenTable.objects.filter(user_token=request.META["HTTP_AUTHORIZATION"]).exists():
                view_kwargs['user_id'] = UserTokenTable.objects.get(
                    user_token=request.META["HTTP_AUTHORIZATION"]).user_id
            else:
                raise Exception("Invalid token provided")

        except Exception as ex:
            response = Response(
                data={"message": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            return response
