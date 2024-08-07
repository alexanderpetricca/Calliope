from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from entries.models import Entry


class EntryViewTests(TestCase):
    
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
        
        # Create 'yesterday' entry
        cls.yesterdayentry = Entry.objects.create(
            created_by = cls.user,
            content = 'Test Entry',
        )
        cls.yesterdayentry.created_at = timezone.now() - timedelta(1)
        cls.yesterdayentry.save()


    # Entries List ----

    def test_entry_list_view_logged_out(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to 
        access the entry list view.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_entry_list'))
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
        
        response = self.client.get(reverse('entries_entry_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-list.html')
        self.assertContains(response, 'Calliope | Entries')


    # Entries List Search ----

    def test_entry_list_view_search_results_logged_in(self):
        """
        Tests the entry list view page is returned when user is logged in, 
        with a search query that SHOULD return results.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        response = self.client.get(reverse('entries_entry_list') + '?search=test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-list.html')
        self.assertContains(response, 'Calliope | Entries')
        self.assertContains(response, self.yesterdayentry.created_at.date().strftime('%d'))


    def test_entry_list_view_search_no_results_logged_in(self):
        """
        Tests the entry list view page is returned when user is logged in, 
        with a search query that SHOULD NOT return results.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        response = self.client.get(reverse('entries_entry_list') + '?search=something')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-list.html')
        self.assertContains(response, 'Calliope | Entries')
        self.assertNotContains(response, self.yesterdayentry.created_at.date().strftime('%d'))


    # Create Entry / Redirect ----

    def test_entry_create_view_logged_out(self):
        """
        Tests user is redirected to login when signed out, whilst trying to 
        access the new entry page.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('entries_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry-create/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry-create/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_entry_create_view_logged_in(self):
        """
        Tests the entry create view page redirects to todays entry when user 
        is logged in, creating the entry if it doesnt exist.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        
        # Test todays entry is created, and redirected to write view, if entry 
        # todays does not exist.
        response = self.client.get(reverse('entries_create'))        
        self.assertEqual(response.status_code, 302)

        todays_entry = Entry.objects.get(created_at__date=timezone.now().date())
        self.assertIsNotNone(todays_entry.id)
        self.assertRedirects(response, reverse('entry_write', kwargs={'pk': f'{todays_entry.id}'}))

        # Test redirected to write view for todays existing entry
        response = self.client.get(reverse('entries_create'))        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('entry_write', kwargs={'pk': f'{todays_entry.id}'}))


    # Entry Detail ----

    def test_entry_detail_view_logged_out(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to 
        access the entry detail view.
        """

        response = self.client.get(reverse('entry_detail', kwargs={'pk': self.yesterdayentry.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry/{self.yesterdayentry.id}/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry/{self.yesterdayentry.id}/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_entry_detail_view_logged_in(self):
        """
        Tests the entry detail view page is returned when user is logged in.
        """ 

        self.client.login(email="testuser@email.com", password="testpass123")

        response = self.client.get(reverse('entry_detail', kwargs={'pk': self.yesterdayentry.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-detail.html')
        self.assertContains(response, f'Calliope | View Entry: {self.yesterdayentry.created_at.strftime("%B %d, %Y")}')


    # Delete Entry ----

    def test_entry_delete_view_logged_out(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to 
        access the entry delete view.
        """

        response = self.client.get(reverse('entries_delete', kwargs={'pk': self.yesterdayentry.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/entry-delete/{self.yesterdayentry.id}/")
        
        response = self.client.get(f"{reverse('login')}?next=/entry-delete/{self.yesterdayentry.id}/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_entry_delete_view_logged_in(self):
        """
        Tests the entry delete view page is returned when user is logged in.
        """ 

        self.client.login(email="testuser@email.com", password="testpass123")
        
        # Test confirmation page
        response = self.client.get(reverse('entries_delete', kwargs={'pk': self.yesterdayentry.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry-delete.html')
        self.assertContains(response, f'Calliope | Delete Entry')

        # Test deletion
        response = self.client.post(reverse('entries_delete', kwargs={'pk': self.yesterdayentry.id}))
        self.assertEqual(response.status_code, 302)

        entries = Entry.objects.filter(deleted=True)
        self.assertTrue(entries.count(), 1)


    # AI Prompt ----
