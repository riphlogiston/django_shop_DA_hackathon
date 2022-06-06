from django.urls import path

from .views import RegistrationView, ActivationView, LoginView, LogoutView, ForgetPasswordView, ChangePasswordView


urlpatterns=[
    path('register/',RegistrationView.as_view()),
    path('activate/<str:activation_code>/',ActivationView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('forget_password/', ForgetPasswordView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
]