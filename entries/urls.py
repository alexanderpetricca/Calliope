from django.urls import path
from . import views 


urlpatterns = [
    path('', views.entry_list_view, name='entries_entry_list'),
    path('entry-create/', views.entry_create_redirect_view, name='entries_create'),
    path('entry/<str:pk>/', views.entry_detail_view, name='entry_detail'),
    path('entry-write/<str:pk>/', views.entry_write_view, name='entry_write'),
    
    path('entry-delete/<str:pk>/', views.entry_delete_view, name='entries_delete'),
    path('entry-limit-reached/', views.entry_limit_reached_view, name='entries_entry_limit'),
]

htmx_patterns = [
    # path('entry-ai-prompt/<str:pk>/', views.entry_ai_prompt_view, name='entries_ai_prompt'),
]

urlpatterns += htmx_patterns