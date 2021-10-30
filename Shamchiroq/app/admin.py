from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'date_of_birth',
        'phone_number', 'gender', 'created_at',
        'updated_at', 'card_number', 'voice')


admin.site.register(User, UserAdmin)
admin.site.register(Voice)
admin.site.register(Subscription)
admin.site.register(Payment)
admin.site.register(Verify)
admin.site.register(Audio)
