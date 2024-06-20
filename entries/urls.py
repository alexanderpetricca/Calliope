from django.urls import path
from . import views 


urlpatterns = [
    path('', views.app_home_view, name='entries_app_home'),
]

htmx_patterns = [
    path('entry-list/', views.entry_list_view, name='entries_entry_list'),
    path('entry-create/', views.entry_create_redirect_view, name='entries_create'),
    path('entry/<str:pk>/', views.entry_view, name='entries_entry'),
    path('entry-message-reply/', views.entry_message_reply_view, name='entries_message_reply'),
    path('entry-delete/<str:pk>/', views.entry_delete_view, name='entries_delete'),
    path('entry-limit-reached/', views.entry_limit_reached_view, name='entries_entry_limit')
]

urlpatterns += htmx_patterns