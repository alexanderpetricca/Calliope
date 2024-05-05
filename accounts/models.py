import uuid, string, random

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
  
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(gettext_lazy('email address'), unique=True)

    email_confirmed = models.BooleanField(default=False)

    premium = models.BooleanField(default=False)
    premium_start_date = models.DateField(null=True, blank=True)
    premium_renewal_date = models.DateField(null=True, blank=True)

    entry_tokens = models.IntegerField(default=4)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    class Meta:
        ordering = ['first_name',]
        verbose_name = "User"
        verbose_name_plural = "Users"


    def replenish_entry_tokens(self):
        """
        Replenishes users tokens - each journal entry costs one token. Trial accounts recieve 4 tokens per month, 
        premium accounts recieve 31 tokens per month.
        """
        
        if self.premium:
            entry_tokens = 31
        else:
            entry_tokens = 4
        self.entry_tokens = entry_tokens
        self.save()


    def use_entry_token(self):
        """
        Deduct a single token from the user account.
        """

        if self.entry_tokens > 0:
            self.entry_tokens -= 1
            self.save()
            return True
        else:
            return False


    def __str__(self):
        return str(self.id)
    

class SignUpCode(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=12, unique=True, editable=False, null=True, blank=True)


    class Meta:
        ordering = ['created',]
        verbose_name = 'Signup Code'
        verbose_name_plural = 'Signup Codes'


    def generate_code(self, length=12):
        """
        Generate a unique code.
        """
        
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if not SignUpCode.objects.filter(code=code).exists():
                return code
            

    def save(self, *args, **kwargs):
        
        if self._state.adding and not self.code:
            self.code = self.generate_code()
        
        super(SignUpCode, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.code)
    

class EmailConfirmationToken(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    email = models.EmailField(null=True, blank=True)


    def __str__(self):
        return self.user.email