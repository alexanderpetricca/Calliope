from django.test import TestCase
from django.contrib.auth import get_user_model

from entries.models import Entry, EntryMessage


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
            owner = self.user,
        )

        self.entry_message = EntryMessage.objects.create(
            entry = self.entry,
            body = 'This is a test message.',
            system_reply = False,
        )


    # Entry ----

    def test_create_entry_obj(self):
        """
        Tests entry object creation.
        """

        self.assertEqual(self.entry.owner.email, 'testuser@email.com')
        self.assertEqual(self.entry.favourite, False)
        self.assertEqual(self.entry.deleted, False)
        self.assertEqual(self.entry.deleted_datetime, None)


    def test_entry_string_representation(self):
        """
        Tests the entry object __str__ method.
        """

        self.assertEqual(str(self.entry), f'{self.entry.owner.id}-{self.entry.created}')


    # Entry Messages ----

    def test_entry_message_obj(self):
        """
        Tests entry message object creation.
        """

        self.assertEqual(self.entry_message.entry.id, self.entry.id)
        self.assertIsNotNone(self.entry_message.created)
        self.assertEqual(self.entry_message.body, 'This is a test message.')
        self.assertFalse(self.entry_message.system_reply)


    def test_entry_message_string_representation(self):
        """
        Tests the entry_message object __str__ method.
        """

        self.assertEqual(str(self.entry_message), str(self.entry_message.id))
