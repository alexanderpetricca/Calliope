from django.test import TestCase
from django.urls import reverse


class PagesTests(TestCase):

    def testLandingPageView(self):
        """Tests the pages landing view & template."""
        
        self.client.logout()
        response = self.client.get(reverse('pages_landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/landing.html')
        self.assertContains(response, 'Calliope | Welcome')

    
    def testFeaturePageView(self):
        """Tests the pages feature view & template."""
        
        self.client.logout()
        response = self.client.get(reverse('pages_features'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/feature-list.html')
        self.assertContains(response, 'Calliope | Features')


    def testPricingPageView(self):
        """Tests the pages pricing view & template."""
        
        self.client.logout()
        response = self.client.get(reverse('pages_pricing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/pricing.html')
        self.assertContains(response, 'Calliope | Pricing')