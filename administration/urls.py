from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login1, name='login'),
    path('signup/', views.signup, name='signup'),
    path('verifyemail/', views.verifyEmail, name='verifyemail'),
    path("generate-otp/", views.generate_otp, name="generate_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("success/", views.success_page, name="success_page"),
    path("newpassword/", views.newpassword, name="newpassword"),
]
