from django.urls import path
from . import views 


urlpatterns = [
    path('', views.appHomeView, name='entries_app_home'),
]

htmx_patterns = [
    path('entry-list/', views.entryListView, name='entries_entry_list'),
    path('entry-create/', views.entryCreateRedirectView, name='entries_create'),
    path('entry/<str:pk>/', views.entryView, name='entries_entry'),
    path('entry-message-reply/', views.entryMessageReplyView, name='entries_message_reply'),
    path('entry-delete/<str:pk>/', views.entryDeleteView, name='entries_delete')
]

urlpatterns += htmx_patterns