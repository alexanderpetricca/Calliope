from django.shortcuts import render


def featuresView(request):

    return render(request, 'pages/features.html')


def pricingView(request):

    return render(request, 'pages/pricing.html')