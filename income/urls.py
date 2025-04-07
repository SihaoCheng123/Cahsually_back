from income.views.income_view import CreateIncomeView, GetUserIncomeListView
from django.urls import path

urlpatterns = [
    path("make-income/<slug:slug>/", CreateIncomeView.as_view(), name="make-income"),
    path("get-income-list/<slug:slug>/", GetUserIncomeListView.as_view(), name="get-user-income-list")
]