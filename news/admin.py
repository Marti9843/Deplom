from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published')
    list_filter = ('date_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_published'
    ordering = ('-date_published',)

admin.site.register(News, NewsAdmin)