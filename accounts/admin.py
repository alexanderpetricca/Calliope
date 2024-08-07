from django.contrib import admin

from .models import CustomUser, SignUpCode, EmailConfirmationToken

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserAdminChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserAdminChangeForm
    fieldsets = (
        (None, {'fields': (
            'email', 
            'password', 
            )}),

        (_('Personal info'), 
            {'fields': (
                'first_name', 
                'last_name',
                )}),

        (_('Account'), 
            {'fields': (
                'premium', 
                'premium_start_date',
                'premium_renewal_date',
                'entry_tokens',
                )}),

        (_('Permissions'), 
            {'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions',
                )}),

        (_('Important dates'), {'fields': (
            'last_login', 
            'date_joined',
            )}),
    )

    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
                ),
            'fields': (
                'email', 
                'password1', 
                'password2', 
                'first_name', 
                'last_name', 
                )}),
    )

    list_display = ['email', 'first_name', 'last_name', 'is_staff',]
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)


class CustomSignUpCodeAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('code', 'created',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SignUpCode, CustomSignUpCodeAdmin)
admin.site.register(EmailConfirmationToken)