from django.contrib import admin
from .models import Entry, EntryMessage


admin.site.register(Entry)
admin.site.register(EntryMessage)
