from django.contrib import admin

from apps.education.models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "created"]
    list_filter = ["created_by"]
    search_fields = ["name", "description", "created_by__email", "created_by__username"]
    date_hierarchy = "created"
    actions = ["mark_searchable", "mark_not_searchable"]
