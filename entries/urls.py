from django.urls import path
from . import views 


app_name = "entries"
urlpatterns = [
    path('', views.appHomeView, name='app_home'),
]

htmx_patterns = [
    path('entry-list', views.entryListView, name='entry_list'),
    path('entry/<str:pk>/', views.entryDetailView, name='entry_detail'),
    path('new/', views.entryCreateView, name='entry_new'),
    path('update/<str:pk>/', views.entryUpdateView, name='entry_update'),
    # path('delete/<str:pk>/', views.entryDeleteView, name='entry_delete'),
    # path('bookmark/<str:pk>/', views.toggleBookmarkView, name='toggle_bookmark'),
]

urlpatterns += htmx_patterns