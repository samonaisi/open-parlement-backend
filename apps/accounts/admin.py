from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "last_login",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    exclude = ("user_permissions", "groups")


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
