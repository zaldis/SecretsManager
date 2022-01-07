from django.contrib import admin

from .models import Secret


class SecretAdmin(admin.ModelAdmin):
    readonly_fields = ['password']


admin.site.register(Secret, SecretAdmin)
