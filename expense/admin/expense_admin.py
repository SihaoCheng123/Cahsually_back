from django.contrib import admin
from expense.models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'account')
    search_fields = ('account__name',)
    ordering = ('date',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Expense, ExpenseAdmin)