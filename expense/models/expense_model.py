from django.db import models

from accounts.models import Account

CATEGORIES = [
    ('food', 'Food'),
    ('payments', 'Payments'),
    ('house', 'House'),
    ('transportation', 'Transportation'),
    ('clothing', 'Clothing'),
    ('health', 'Health'),
    ('entertainment', 'Entertainment'),
    ('others', 'Others')
]

class Expense(models.Model):
    category = models.CharField(max_length=50, choices=CATEGORIES, default="others", verbose_name="Expense category")
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Amount", null=False)
    date = models.DateTimeField()
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name="Description")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="expense", verbose_name="Account from expense")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last update')

    class Meta:
        db_table = "expense"
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.category}"