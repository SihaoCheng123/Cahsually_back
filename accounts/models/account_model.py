from django.db import models
from users.models import CustomUser
from django.utils.text import slugify

class Account(models.Model):
    name = models.CharField(max_length=50, null=False, verbose_name="Account name")
    balance = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Account balance", null=False)
    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="accounts", null=False)
    slug = models.SlugField(max_length=50, unique=True, verbose_name="slug", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last update')

    class Meta:
        db_table = "accounts"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            cont = 1

            while Account.objects.filter(slug=slug).exists():
                slug = f"{slug}-{cont}"
                cont+=1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"