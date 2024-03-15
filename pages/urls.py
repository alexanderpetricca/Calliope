from django.urls import path
from . import views 


urlpatterns = [
    path('', views.landingPageView, name='pages_landing'),
    path('features/', views.featuresView, name='pages_features'),
    path('pricing/', views.pricingView, name='pages_pricing'),
]