from django.contrib import admin
from .models import Project, Screenshot

class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published", "sort_order")
    list_editable = ("published", "sort_order")
    list_filter = ("category", "published")
    search_fields = ("title", "summary", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ScreenshotInline]
    fieldsets = (
        ("Project", {"fields": ("title", "slug", "summary", "category", "status", "technologies")}),
        ("The story", {"fields": ("description", "works_today", "next_steps", "limitations", "contribution")}),
        ("Links and instructions", {"fields": ("source_url", "demo_url", "demo_label", "download_url", "controls", "run_instructions")}),
        ("Visibility", {"fields": ("published", "sort_order")}),
    )
