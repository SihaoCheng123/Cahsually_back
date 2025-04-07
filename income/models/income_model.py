from django.db import models

from accounts.models import Account


class Income(models.Model):
    concept = models.CharField(max_length=100, null=False, blank=False, verbose_name="Concept")
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Amount", null=False)
    date = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="income", verbose_name="Account from expense")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last update')

    class Meta:
        db_table = "income"
        verbose_name= "Income"
        verbose_name_plural = "Incomes"

    def __str__(self):
        return f"{self.concept}"