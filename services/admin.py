from django.contrib import admin
from .models import Service, Activity, Trainer

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type')
    search_fields = ('name',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'service')
    list_filter = ('service',)
    search_fields = ('name',)

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization')
    search_fields = ('full_name', 'specialization')