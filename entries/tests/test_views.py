from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from entries.models import Entry


class ArtworkDesignViewTests(TestCase):
    
    @classmethod
    def setUpTestData(self):

        # Create Test User        
        self.user = get_user_model().objects.create_user(
            username = "TestUser",
            email = "testuser@email.com",
            first_name = "Test",
            last_name = "User",
            password = "testpass123",
        )
        
        # Create Entry Job
        self.artworkjob = Entry.objects.create(
            author = self.user,
            body = 'This is some test content.',
        )


    # App Home
    def testEntryListViewLoggedOut(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the entry list view.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_app_home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/app/")
        
        response = self.client.get(f"{reverse('login')}?next=/app/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def testEntryListViewLoggedIn(self):
        """
        Tests the entry list view page is returned when user is logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_app_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/home.html')
        self.assertContains(response, 'Calliope | Home')


    # HTMX List View
    # HTMX Search View
    # HTMX Create View
    # HTMX Update View
    # HTMX Delete View