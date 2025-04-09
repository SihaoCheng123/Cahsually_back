
from django.urls import path

from expense.serializers import GetUserExpenseListView
from expense.views import CreateExpenseView, GetExpenseListByMonthView

urlpatterns = [
    path("make-expense/<slug:slug>/", CreateExpenseView.as_view(), name="make-expense"),
    path("get-expense-list/<slug:slug>/", GetUserExpenseListView.as_view(), name="get-user-expense-list"),
    path("get-expense-month/<slug:slug>/", GetExpenseListByMonthView.as_view(), name="month-expense")
]