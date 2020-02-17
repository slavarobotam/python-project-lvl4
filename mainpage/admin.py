from django.contrib import admin

from mainpage.models import Status, Tag, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'creator', 'assigned_to')
    list_filter = ('name', 'status', 'creator', 'assigned_to')
    search_fields = ('name', 'description')
    raw_id_fields = ('creator',)
    ordering = ('status', 'creator')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_value',)
