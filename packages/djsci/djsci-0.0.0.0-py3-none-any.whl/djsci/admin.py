from django.contrib import admin

from .models import PrivateFile


class PrivateFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(PrivateFile, PrivateFileAdmin)
