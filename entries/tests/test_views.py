from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from entries.models import Entry, EntryMessage


class entryviewTests(TestCase):
    
    @classmethod
    def setUp(cls):

        # Create Test User        
        cls.user = get_user_model().objects.create_user(
            username = "TestUser",
            email = "testuser@email.com",
            first_name = "Test",
            last_name = "User",
            password = "testpass123",
        )
        
        # Create entry
        cls.entry = Entry.objects.create(
            created_by = cls.user,
        )

        # Create entry Message
        cls.entry_message = EntryMessage.objects.create(
            entry = cls.entry,
            body = 'This is a test message.',
            system_reply = False,
        )

        # Create 'yesterday' entry
        cls.yesterdayentry = Entry.objects.create(
            created_by = cls.user,
        )
        cls.yesterdayentry.created_at = timezone.now() - timedelta(1)
        cls.yesterdayentry.save()


    # App Home ----

    def test_entry_list_view_logged_out(self):
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


    def test_entry_list_view_logged_in(self):
        """
        Tests the entry list view page is returned when user is logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_app_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/home.html')
        self.assertContains(response, 'Calliope | Home')


    # HTMX entry List ----

    def test_htmx_entry_list_view_logged_out(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the entry list htmx endpoint.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_entry_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry-list/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry-list/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_htmx_entry_list_view_logged_in_non_htmx(self):
        """
        Tests a 403 is returned when trying to access the htmx entry list endpoint, when logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_entry_list'))
        self.assertEqual(response.status_code, 403)


    def test_entry_list_view_logged_in(self):
        """
        Tests the entry list view page is returned when user is logged in (with htmx).
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


    def test_entry_list_view_search_logged_In(self):
        """
        Tests the entry list view page is returned when user is logged in (with htmx), with a search query that SHOULD 
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
        self.assertContains(response, self.entry.created_at.date().strftime('%B %d, %Y'))


    def test_entry_List_view_search_no_results_loggedIn(self):
        """
        Tests the entry list view page is returned when user is logged in (with htmx), with a search query that SHOULD 
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
        self.assertNotContains(response, self.entry.created_at.date().strftime('%B %d, %Y'))


    # htmx Create Redirect ----

    def test_htmx_entry_create_view_logged_Out(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the new entry htmx endpoint.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry-create/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry-create/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_htmx_entry_create_view_logged_In_non_htmx(self):
        """
        Tests a 403 is returned when trying to access the htmx entry create endpoint, when logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_create'))
        self.assertEqual(response.status_code, 403)


    def test_entry_create_view_logged_in(self):
        """
        Tests the entry create view page redirects to todays entry when user is logged in (with htmx).
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


    # htmx entry view ----

    def test_htmx_entry_view_logged_out(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to access the entry htmx endpoint.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_entry', kwargs={'pk': f'{self.entry.id}'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry/{self.entry.id}/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry/{self.entry.id}/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_htmx_entry_view_logged_In_non_htmx(self):
        """
        Tests a 403 is returned when trying to access the entry htmx endpoint, when logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('entries_entry', kwargs={'pk': f'{self.entry.id}'}))
        self.assertEqual(response.status_code, 403)


    def test_entry_view_logged_In(self):
        """
        Tests the entry view page returns the requested entry when user is logged in (with htmx).
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


    def test_entry_view_logged_In_previous_entry(self):
        """
        Tests the entry view page does NOT render message form, when showing an entry that was not created today 
        (with htmx).
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        headers = {
            'HX-Request': 'true',
            'Content-Type': 'text/html',
        }

        response = self.client.get(
            reverse('entries_entry', kwargs={'pk': f'{self.yesterdayentry.id}'}),
            **{'HTTP_' + k.replace('-', '_').upper(): v for k, v in headers.items()}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry.html')
        self.assertNotContains(response, 'id="entry_msg_create_form"')


    def test_entry_view_logged_in_post(self):
        """
        Tests the entry view page renders a new message when a POST request is sent via htmx.
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

       
    # htmx Delete view ----
    # htmx entry Limit view ----
