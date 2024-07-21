from django.test import TestCase
from django.contrib.auth import get_user_model

from entries.models import Entry


class EntriesModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'TestUser',
            first_name = 'Test',
            last_name = 'User',
            email = 'testuser@email.com',
            password = 'testpass123'
        )

        self.entry = Entry.objects.create(
            created_by = self.user,
        )


    # Entry ----

    def test_create_entry_model(self):
        """
        Tests entry object creation.
        """

        self.assertIsNotNone(self.entry.id)
        self.assertIsNotNone(self.entry.created_at)
        self.assertEqual(self.entry.created_by.email, 'testuser@email.com')
        self.assertEqual(self.entry.favourite, False)
        self.assertEqual(self.entry.deleted, False)
        self.assertEqual(self.entry.deleted_at, None)


    def test_entry_model_str_method(self):
        """
        Tests the entry object __str__ method.
        """

        self.assertEqual(str(self.entry), f'Test User-{self.entry.created_at}')
