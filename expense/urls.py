
from django.urls import path

from expense.serializers import GetUserExpenseListView
from expense.views import CreateExpenseView

urlpatterns = [
    path("make-expense/<slug:slug>/", CreateExpenseView.as_view(), name="make-expense"),
    path("get-expense-list/<slug:slug>/", GetUserExpenseListView.as_view(), name="get-user-expense-list")
]