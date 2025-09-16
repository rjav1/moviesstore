from django.contrib import admin
from .models import Movie, Review, ReviewFlag

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "flags_count", "is_hidden", "date")
    list_filter = ("is_hidden", "movie")
    search_fields = ("comment", "user__username", "movie__name")
    actions = ["hide_selected", "unhide_selected"]

    def hide_selected(self, request, queryset):
        queryset.update(is_hidden=True)
    def unhide_selected(self, request, queryset):
        queryset.update(is_hidden=False)

admin.site.register(Movie, MovieAdmin)
admin.site.register(ReviewFlag)
