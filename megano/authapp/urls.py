from django.urls import path
from authapp import views

urlpatterns = [
    path("sign-in/", views.SignInView.as_view(), name="signin"),
    path("sign-up/", views.SignUpView.as_view(), name="signup"),
    path("sign-out/", views.sign_out, name="signout")
]