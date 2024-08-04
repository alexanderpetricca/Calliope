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
            content = 'Some test content.'
        )


    # Entry ----

    def test_create_entry_model(self):
        """
        Tests entry object creation.
        """

        self.assertIsNotNone(self.entry.id)
        self.assertIsNotNone(self.entry.created_at)
        self.assertEqual(self.entry.created_by.email, 'testuser@email.com')
        self.assertEqual(self.entry.content, 'Some test content.')
        self.assertIsNone(self.entry.prompt)
        self.assertFalse(self.entry.favourite)
        self.assertFalse(self.entry.deleted)
        self.assertIsNone(self.entry.deleted_at)


    def test_entry_model_str_method(self):
        """
        Tests the entry object __str__ method.
        """

        self.assertEqual(str(self.entry), f'Test User-{self.entry.created_at}')


    def test_entry_soft_delete_method(self):
        """
        Tests the soft_delete method on the Entry model.
        """

        self.entry.soft_delete()

        self.assertTrue(self.entry.deleted)
        self.assertIsNotNone(self.entry.deleted_at)


    def test_entry_restore_soft_delete_method(self):
        """
        Tests the restore_soft_delete method on the Entry model.
        """

        self.entry.soft_delete()
        self.entry.restore_soft_delete()

        self.assertFalse(self.entry.deleted)
        self.assertIsNone(self.entry.deleted_at)


    def test_entry_toggle_favourite_method(self):
        """
        Tests the toggle_favourite method on the Entry model.
        """

        self.entry.toggle_favourite()
        self.assertTrue(self.entry.favourite)

        self.entry.toggle_favourite()
        self.assertFalse(self.entry.favourite)