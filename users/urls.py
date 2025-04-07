from django.urls import path
from users.views import RegisterView, DeleteUserView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("delete/<slug:slug>/", DeleteUserView.as_view(), name="delete-user"),
    path("login/", LoginView.as_view(), name="login")
]