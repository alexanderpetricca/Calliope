from django.urls import include, path

from . import views


urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='view_profile'),
    path('update-profile/<str:pk>/',views.UpdateUserProfileView.as_view(), name='update_profile'),

    # Password and Account Management
    path('password/change-done/', views.PasswordChangeDoneView.as_view(),name='change_password_done'),
    path('password/change/', views.CustomPasswordChangeView.as_view(),name='change_password'),
    path('', include('allauth.urls')),
]