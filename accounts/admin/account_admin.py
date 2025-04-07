from django.contrib import admin
from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'users', 'slug')
    search_fields = ('users__name',)
    ordering = ('created_at',)
    readonly_fields = ('created_at', 'updated_at','slug')


admin.site.register(Account, AccountAdmin)