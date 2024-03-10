from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class CustomUserTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username = 'TestUser',
            first_name = 'Test',
            last_name = 'User',
            email = 'testuser@email.com',
            password = 'testpass123'
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username = 'superadmin',
            first_name = 'Super',
            last_name = 'Admin',
            email = 'superadmin@email.com',
            password = 'testpass123'
            )

        self.add_customuser = Permission.objects.get(codename='add_customuser')
        self.view_customuser = Permission.objects.get(codename='view_customuser')

    # Tests user creation
    def test_create_user(self):
        self.assertEqual(self.user.username, 'TestUser')
        self.assertEqual(self.user.email, 'testuser@email.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)


    # Tests super user creation
    def test_create_superuser(self):
        self.assertEqual(self.admin_user.username, 'superadmin')
        self.assertEqual(self.admin_user.email, 'superadmin@email.com')
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)


    #Tests the string return method
    def test_string_representation(self):
        self.assertEqual(str(self.user), "testuser@email.com")
        self.assertEqual(str(self.admin_user), "superadmin@email.com")