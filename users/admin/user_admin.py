from users.models import CustomUser
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    model = CustomUser

    list_display = ('name', 'email', 'phone', 'age', 'is_active', 'slug')
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    search_fields = ('name', 'email',)
    readonly_fields = ("slug",)
    ordering = ('email',)

    fieldsets = (
        ('User data', {'fields': ('name', 'email', 'phone', 'password', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        ("User creation", {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk and obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, UserAdmin)