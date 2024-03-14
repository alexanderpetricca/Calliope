from django.shortcuts import render


def landingPageView(request):

    return render(request, 'pages/landing.html')


def featuresView(request):

    return render(request, 'pages/features.html')


def pricingView(request):

    return render(request, 'pages/pricing.html')