from django.urls import path
from .views import ChangePhoneNumber, ChangePhoneNumberConfirm, ChangePhoneNumberVerifyCode, RegisterView, PhoneView, OtpView,  LoginView, CreateView,  MyOrders, ChangePasswordView, ResetPasswordConfirm, ResetPasswordVerifyCode, ResetPasswordView, SendSms, UserDetailView

urlpatterns=[
    path('register/', RegisterView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('password/reset/', ResetPasswordView.as_view()),
    path('password/reset/verify/code/', ResetPasswordVerifyCode.as_view()),
    path('password/reset/confirm/', ResetPasswordConfirm.as_view()),

    path('phone/', PhoneView.as_view()),
    path('otp/', OtpView.as_view()),
    path('login/', LoginView.as_view()),
    path('create/', CreateView.as_view()),
    path('my_orders/', MyOrders.as_view()),
    path('user-detail/<int:pk>/', UserDetailView.as_view()),

    path('change_phone_number/', ChangePhoneNumber.as_view()),
    path('change_phone_number/verify/code/', ChangePhoneNumberVerifyCode.as_view()),
    path('change_phone_number/confirm/', ChangePhoneNumberConfirm.as_view()),


    path("send_sms/", SendSms.as_view()),
]