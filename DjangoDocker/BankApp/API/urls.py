from django.urls import path

from API.views.auth_view import RegisterView, VerifyEmailView, LoginView
from API.views.profile_view import ProfileView, UserPicView, UserPasswordView
from API.views.reset_password import ForgetPasswordView, reset_password_view, update_password_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('picture/', UserPicView.as_view(), name='picture'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update/password/', update_password_view, name='reset'),
    path('password/', UserPasswordView.as_view(), name='password'),
    path('forget/password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('password/reset/<str:verification_code>/', reset_password_view, name='password_reset'),
    path('verify/account/<str:verification_code>/', VerifyEmailView.as_view(), name='verify_email'),
]
