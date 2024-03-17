from django.urls import path

from . import views


urlpatterns = [
    
    path('login/', views.customLoginPageView, name='login'),
    path('logout/', views.customLogoutPageView, name='logout'),
    
    path('profile/', views.userProfileView, name='view_profile'),
    path('update-profile/<str:pk>/',views.updateUserProfileView, name='update_profile'),

    # Password and Account Management
    # path('password/change-done/', views.PasswordChangeDoneView.as_view(),name='change_password_done'),
    # path('password/change/', views.CustomPasswordChangeView.as_view(),name='change_password'),
]