import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy


class CustomUser(AbstractUser):
  
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(gettext_lazy('email address'), unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    class Meta:
        ordering = ['first_name',]
        verbose_name = "User"
        verbose_name_plural = "Users"


    def __str__(self):
        return self.email



