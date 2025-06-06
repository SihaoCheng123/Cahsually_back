from django.urls import path
from accounts.views import CreateAccountView, DeleteAccountView, GetAccountsByUser, GetOperationListView
urlpatterns = [
    path("create-account/<slug:slug>/", CreateAccountView.as_view(), name="create-account"),
    path("delete-account/<slug:slug>/", DeleteAccountView.as_view(), name="delete-account"),
    path("get-all-accounts/<slug:slug>/", GetAccountsByUser.as_view(), name="get-all-accounts"),
    path("get-operation-list/<slug:slug>/", GetOperationListView.as_view(), name="get-operation-list")
]