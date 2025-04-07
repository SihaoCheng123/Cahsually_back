from django.contrib import admin
from income.models import Income

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('concept', 'amount', 'date', 'account')
    search_fields = ('account__name',)
    ordering = ('date',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Income, IncomeAdmin)