from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('username',)


admin.site.register(User, UserAdmin)