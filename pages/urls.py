from django.urls import path
from . import views 


urlpatterns = [
    path('', views.LandingPageView.as_view(), name='pages_landing'),
    path('features/', views.FeaturesPageView.as_view(), name='pages_features'),
    path('pricing/', views.PricingPageView.as_view(), name='pages_pricing'),
]