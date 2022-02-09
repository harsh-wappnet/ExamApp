from django.urls import path

from Auth.views import LoginView, RegisterView, VerifyEmailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/account/<str:verification_code>/', VerifyEmailView.as_view(), name='verify_email'),
]
