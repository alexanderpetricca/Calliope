from django.urls import path
from . import views 


app_name = "pages"
urlpatterns = [
    path('', views.landingPageView, name='landing'),
    path('features/', views.featuresView, name='features'),
    path('pricing/', views.pricingView, name='pricing'),
]