import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy


class CustomUser(AbstractUser):
  
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(gettext_lazy('email address'), unique=True)

    premium = models.BooleanField(default=False)
    premium_monthly = models.BooleanField(default=False)
    premium_paid_date = models.DateField(null=True, blank=True)

    tokens = models.IntegerField(default=4)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    class Meta:
        ordering = ['first_name',]
        verbose_name = "User"
        verbose_name_plural = "Users"


    def replenishTokens(self):
        """
        Replenishes users tokens - each journal entry costs one token. Trial accounts recieve 4 tokens per month, 
        premium accounts recieve 31 tokens per month.
        """
        
        if self.premium:
            tokens = 31
        else:
            tokens = 4
        self.tokens = tokens
        self.save()


    def useToken(self):
        """
        Deduct a single token from the user account.
        """

        self.tokens -= 1
        self.save()


    def __str__(self):
        return str(self.id)
    

class SignUpcode(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=12, unique=True, editable=False, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    used = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


    class Meta:
        ordering = ['created',]
        verbose_name = 'Signup Code'
        verbose_name_plural = 'Signup Codes'


    def generateCode(self):
        pass


    def __str__(self):
        return str(self.id)



