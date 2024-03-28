from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import forms

from . import views


urlpatterns = [
    
    path('login/', views.customLoginPageView, name='login'),
    path('logout/', views.customLogoutPageView, name='logout'),
    
    path('signup/', views.customSignupView, name='signup'),

    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=forms.CustomPasswordResetForm), name='password_reset'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(form_class=forms.CustomSetPasswordForm),
            name='password_reset_confirm'),
    
    path('password_change/', views.customPasswordChangeView, name='password_change'),
    path('password_change/done/', views.customPasswordChangeDoneView, name='password_change_done'),
    
    path('profile/', views.userProfileView, name='view_profile'),
    path('update-profile/',views.updateUserProfileView, name='update_profile'),
]