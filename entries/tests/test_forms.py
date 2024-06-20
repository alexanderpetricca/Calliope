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


    def test_entry_message_create_form(self):
        """
        Tests entry message create form functionality.
        """
        
        form_data = {
            'body': 'This is some test content.',
        }
        
        form = forms.EntryMessageCreateForm(data=form_data, files=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['body'], 'This is some test content.')