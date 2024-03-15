from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid


class Entry(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    body = models.TextField(null=True, blank=True)
    favourite = models.BooleanField(default=False)

    deleted = models.BooleanField(default=False)
    deleted_datetime = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ['-created']
        verbose_name = "Entry"
        verbose_name_plural = "Entries"


    def __str__(self):
        return f'{self.author}-{self.created}'


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
    



