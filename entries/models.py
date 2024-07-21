import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone


class Entry(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    content = models.TextField()

    favourite = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"


    def __str__(self):
        return f'{self.created_by}-{self.created_at}'


    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()


    def restore_soft_delete(self):
        self.deleted = False
        self.deleted_at = None
        self.save()

    
    def toggle_favourite(self):
        self.favourite = not self.favourite
        self.save()


    def get_absolute_url(self):
        return reverse('entries_entry_detail', args=[str(self.id)])
    

# class EntryMessage(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     entry = models.ForeignKey(
#         Entry,
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True,
#         related_name='messages',
#     )
#     body = models.TextField(max_length=1000)
#     system_reply = models.BooleanField(default=False)


#     class Meta:
#         verbose_name = 'Entry Message'
#         verbose_name_plural = 'Entry Messages'


#     def __str__(self):
#         return str(self.id)