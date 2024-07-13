from django.contrib import admin

from advertisements.models import Favorites


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ['user']
