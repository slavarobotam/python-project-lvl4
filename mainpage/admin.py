from django.contrib import admin
from .models import Task, Tag


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
