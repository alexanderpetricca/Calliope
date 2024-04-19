from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from entries.models import Entry, EntryMessage


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

        # Create Entry Message
        cls.entry_message = EntryMessage.objects.create(
            entry = cls.entry,
            body = 'This is a test message.',
            system_reply = False,
        )

        # Create 'yesterday' entry
        cls.yesterdayEntry = Entry.objects.create(
            owner = cls.user,
        )
        cls.yesterdayEntry.created = timezone.now() - timedelta(1)
        cls.yesterdayEntry.save()


    # App Home ----

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


    # HTMX Entry List ----

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
        Tests the entry list view page is returned when user is logged in (with HTMX).
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


    def testEntryListViewSearchLoggedIn(self):
        """
        Tests the entry list view page is returned when user is logged in (with HTMX), with a search query that SHOULD 
        return results.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        response = self.client.get(
            reverse('entries_entry_list') + '?search=test',
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-list.html')
        self.assertContains(response, self.entry.created.date().strftime('%B %d, %Y'))


    def testEntryListViewSearchNoResultsLoggedIn(self):
        """
        Tests the entry list view page is returned when user is logged in (with HTMX), with a search query that SHOULD 
        NOT return results.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        response = self.client.get(
            reverse('entries_entry_list')  + '?search=No%20Results',
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-list.html')
        self.assertNotContains(response, self.entry.created.date().strftime('%B %d, %Y'))


    # HTMX Create Redirect ----

    def testHTMXEntryCreateViewLoggedOut(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the new entry HTMX endpoint.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry-create/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry-create/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def testHTMXEntryCreateViewLoggedInNonHTMX(self):
        """
        Tests a 403 is returned when trying to access the HTMX entry create endpoint, when logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_create'))
        self.assertEqual(response.status_code, 403)


    def testEntryCreateViewViewLoggedIn(self):
        """
        Tests the entry create view page redirects to todays entry when user is logged in (with HTMX).
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        response = self.client.get(
            reverse('entries_create'),
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()}
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('entries_entry', kwargs={'pk': f'{self.entry.id}'}))


    # HTMX Entry View ----

    def testHTMXEntryViewLoggedOut(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the entry HTMX endpoint.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_entry', kwargs={'pk': f'{self.entry.id}'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry/{self.entry.id}/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry/{self.entry.id}/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def testHTMXEntryViewLoggedInNonHTMX(self):
        """
        Tests a 403 is returned when trying to access the entry HTMX endpoint, when logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_entry', kwargs={'pk': f'{self.entry.id}'}))
        self.assertEqual(response.status_code, 403)


    def testEntryViewLoggedIn(self):
        """
        Tests the entry view page returns the requested entry when user is logged in (with HTMX).
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        response = self.client.get(
            reverse('entries_entry', kwargs={'pk': f'{self.entry.id}'}),
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry.html')
        self.assertContains(response, 'id="entry_msg_create_form"')
        self.assertContains(response, 'This is a test message.')


    def testEntryViewLoggedInPreviousEntry(self):
        """
        Tests the entry view page does NOT render message form, when showing an entry that was not created today 
        (with HTMX).
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        response = self.client.get(
            reverse('entries_entry', kwargs={'pk': f'{self.yesterdayEntry.id}'}),
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry.html')
        self.assertNotContains(response, 'id="entry_msg_create_form"')


    def testEntryViewLoggedInPost(self):
        """
        Tests the entry view page renders a new message when a POST request is sent via HTMX.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        data = {
            'body': 'Hello Calliope'
        }

        response = self.client.post(
            reverse('entries_entry', kwargs={'pk': f'{self.entry.id}'},),
            data,
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()},
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/partials/entry-message.html')
        self.assertContains(response, 'Hello Calliope')
    

    # Test user adding a message, and that this triggers an AI response
    # Ensure AI response is loaded into DOM
    # Ensure AI response is marked as system response

       
    # HTMX Delete View ----
    # HTMX Entry Limit View ----
