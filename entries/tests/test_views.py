from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from entries.models import Entry


class EntryViewTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        # Create Test User        
        cls.user = get_user_model().objects.create_user(
            username = "TestUser",
            email = "testuser@email.com",
            first_name = "Test",
            last_name = "User",
            password = "testpass123",
        )
        
        # Create Entry
        cls.entry = Entry.objects.create(
            owner = cls.user,
        )


    # App Home
    def testEntryListViewLoggedOut(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the entry list view.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_app_home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/")
        
        response = self.client.get(f"{reverse('login')}?next=/")
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


    # HTMX Entry List

    def testHTMXEntryListViewLoggedOut(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the entry list HTMX endpoint.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_entry_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry-list/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry-list/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def testHTMXEntryListViewLoggedInNonHTMX(self):
        """
        Tests a 403 is returned when trying to access the HTMX entry list endpoint, when logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_entry_list'))
        self.assertEqual(response.status_code, 403)


    def testEntryListViewLoggedIn(self):
        """
        Tests the entry list view page is returned when user is logged in, with HTMX.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        response = self.client.get(
            reverse('entries_entry_list'), 
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-list.html')


    # HTMX Search View
    # HTMX Entry View
    # HTMX Delete View