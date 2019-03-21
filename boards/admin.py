from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'uploaded_at',)
admin.site.register(Board, BoardAdmin)
