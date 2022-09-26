from django.contrib import admin

from .models import ConfigList, ConfigPair, User


class ConfigPairInline(admin.TabularInline):
    fields = ('key', 'value', 'is_request_data_key')
    model = ConfigPair


@admin.register(ConfigList)
class ConfigListAdmin(admin.ModelAdmin):
    inlines = [ConfigPairInline]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
