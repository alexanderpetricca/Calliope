from django.urls import path
from . import views 


urlpatterns = [
    path('', views.entryListView, name='entries_app_home'),
    path('entry-list/', views.entryListView, name='entries_entry_list'),
    
    path('entry-create/', views.entryCreateView, name='entries_create'),
    path('entry/<str:pk>/', views.entryView, name='entries_entry'),
    path('entry-message-reply/', views.entryMessageReplyView, name='entries_message_reply'),
]

htmx_patterns = []

urlpatterns += htmx_patterns