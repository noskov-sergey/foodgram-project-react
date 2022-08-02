from django.contrib import admin

from .models import FoodgramUser, Subscribe

class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ['username']

admin.site.register(FoodgramUser, FoodgramUserAdmin)

class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
admin.register(Subscribe, SubscribeAdmin)