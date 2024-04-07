from django.contrib import admin
from . import models

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')

admin.site.register(models.Message, ChatAdmin)