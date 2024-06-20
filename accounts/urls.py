from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import forms

from . import views


urlpatterns = [
    
    path('login/', views.custom_login_page_view, name='login'),
    path('logout/', views.custom_logout_page_view, name='logout'),
    
    path('signup/', views.custom_signup_view, name='signup'),

    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=forms.CustomPasswordResetForm), name='password_reset'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(form_class=forms.CustomSetPasswordForm),
            name='password_reset_confirm'),
    
    path('password_change/', views.custom_password_change_view, name='password_change'),
    path('password_change/done/', views.custom_password_change_done_view, name='password_change_done'),
    
    path('profile/', views.user_profile_view, name='view_profile'),
    path('update-profile/',views.update_user_profile_view, name='update_profile'),
    path('update-email/',views.update_user_email_view, name='update_email'),
    path('update-email-sent/',views.update_user_email_sent_view, name='update_email_sent'),
    path('update-email-confirm/<str:pk>/',views.update_user_email_confirm_view, name='update_email_confirm'),
    path('update-email-success/',views.update_user_email_confirm_success, name='update_email_success'),
]