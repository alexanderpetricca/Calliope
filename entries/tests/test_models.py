from django.test import TestCase
from django.contrib.auth import get_user_model

from entries.models import Entry


class EntryModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'TestUser',
            first_name = 'Test',
            last_name = 'User',
            email = 'testuser@email.com',
            password = 'testpass123'
        )

        self.entry = Entry.objects.create(
            owner = self.user,
        )


    # Tests entry creation
    def test_create_entry(self):
        self.assertEqual(self.entry.owner.email, 'testuser@email.com')
        self.assertEqual(self.entry.favourite, False)
        self.assertEqual(self.entry.deleted, False)
        self.assertEqual(self.entry.deleted_datetime, None)


    # Tests the string return method
    def test_string_representation(self):
        self.assertEqual(str(self.entry), f'{self.entry.owner.id}-{self.entry.created}')