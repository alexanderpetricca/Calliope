from django.urls import path

from . import views


urlpatterns = [
    
    path('login/', views.customLoginPageView, name='login'),
    path('logout/', views.customLogoutPageView, name='logout'),
    
    path('signup/', views.customSignupView, name='signup'),
    
    path('password_change/', views.customPasswordChangeView, name='password_change'),
    path('password_change/done/', views.customPasswordChangeDoneView, name='password_change_done'),
    
    path('profile/', views.userProfileView, name='view_profile'),
    path('update-profile/',views.updateUserProfileView, name='update_profile'),

    # Password and Account Management
    # path('password/change-done/', views.PasswordChangeDoneView.as_view(),name='change_password_done'),
    # path('password/change/', views.CustomPasswordChangeView.as_view(),name='change_password'),
]