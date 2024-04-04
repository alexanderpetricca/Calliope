from django.urls import path
from . import views 


urlpatterns = [
    path('', views.appHomeView, name='entries_app_home'),
]

htmx_patterns = [
    path('entry-list/', views.entryListView, name='entries_entry_list'),
    path('entry/<str:pk>/', views.entryDetailView, name='entries_entry_detail'),
    path('new/', views.entryCreateView, name='entries_entry_new'),
    path('update/<str:pk>/', views.entryUpdateView, name='entries_entry_update'),
]

urlpatterns += htmx_patterns