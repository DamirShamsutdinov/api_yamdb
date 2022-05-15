from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
