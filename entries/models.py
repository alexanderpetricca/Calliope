from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid


class Entry(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    favourite = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ['-created']
        verbose_name = "Entry"
        verbose_name_plural = "Entries"


    def __str__(self):
        return f'{self.owner}-{self.created}'


    def softDelete(self):
        self.deleted = True
        self.deleted_datetime = timezone.now()
        self.save()


    def restoreSoftDelete(self):
        self.deleted = False
        self.deleted_datetime = None
        self.save()

    
    def toggleFavourite(self):
        self.bookmarked = not self.bookmarked
        self.save()


    def get_absolute_url(self):
        return reverse('entries_entry_detail', args=[str(self.id)])
    


class EntryMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(max_length=1000)
    system_reply = models.BooleanField(default=False)


    class Meta:
        ordering = ['created',]
        verbose_name = 'Entry Message'
        verbose_name_plural = 'Entry Messages'


    def __str__(self):
        return str(self.id)