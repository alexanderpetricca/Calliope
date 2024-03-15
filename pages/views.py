from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = 'pages/landing.html'


class FeaturesPageView(TemplateView):
    template_name = 'pages/feature-list.html'


class PricingPageView(TemplateView):
    template_name = 'pages/pricing.html'