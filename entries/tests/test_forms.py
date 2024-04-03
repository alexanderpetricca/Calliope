from django.test import TestCase
from django.contrib.auth import get_user_model

from entries import forms


class EntryFormTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username = "TestUser",
            email = "testuser@email.com",
            first_name = "Test",
            last_name = "User",
            password = "testpass123",
        )


    def testEntryCreateJobForm(self):
        """
        Tests entry create form functionality.
        """
        
        form_data = {
            'body': 'This is some test content.',
        }
        
        form = forms.EntryCreateForm(data=form_data, files=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['body'], 'This is some test content.')


    def testEntryUpdateJobForm(self):
        """
        Tests entry update form functionality.
        """
        
        form_data = {
            'body': 'This is some updated test content.',
        }
        
        form = forms.EntryUpdateForm(data=form_data, files=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['body'], 'This is some updated test content.')