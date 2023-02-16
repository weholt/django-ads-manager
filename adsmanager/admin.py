from django.contrib import admin

from .models import Ad, AdClick


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created", "target_link", "link_text", "weight", "display_count", "click_count"]
    list_filter = []
    date_hierarchy = "created"
    readonly_fields = ["creator", "created"]

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(AdClick)
class AdClickAdmin(admin.ModelAdmin):
    list_display = ["ad", "user", "created"]
    list_filter = []
    date_hierarchy = "created"
