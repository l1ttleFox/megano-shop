from django.urls import path
from authapp import views

app_name = "authapp"

urlpatterns = [
    path("sign-in", views.SignInView.as_view(), name="signin"),
    path("sign-up", views.SignUpView.as_view(), name="signup"),
    path("sign-out", views.sign_out, name="signout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path(
        "profile/password", views.ProfilePasswordView.as_view(), name="password_update"
    ),
    path("profile/avatar/", views.AvatarUpdateView.as_view(), name="avatar_update"),
]
