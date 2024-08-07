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


    def test_entry_write_form(self):
        """
        Tests entry create / update functionality.
        """

        form_data = {
            'content': 'This is some test content.',
        }

        form = forms.EntryCreateUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'This is some test content.')