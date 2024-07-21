from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from accounts.models import SignUpCode


class CustomUserModelTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username = 'TestUser',
            first_name = 'Test',
            last_name = 'User',
            email = 'testuser@email.com',
            password = 'testpass123'
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username = 'adminuser',
            first_name = 'Admin',
            last_name = 'User',
            email = 'adminuser@email.com',
            password = 'testpass123'
        )

        self.add_customuser = Permission.objects.get(codename='add_customuser')
        self.view_customuser = Permission.objects.get(codename='view_customuser')


    def test_create_user(self):
        """
        Test user object creation.
        """        

        self.assertEqual(self.user.username, 'TestUser')
        self.assertEqual(self.user.email, 'testuser@email.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertFalse(self.user.email_confirmed)
        self.assertEqual(self.user.entry_tokens, 4)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)


    def test_create_superuser(self):
        """
        Test user object superuser creation.
        """

        self.assertEqual(self.admin_user.username, 'adminuser')
        self.assertEqual(self.admin_user.email, 'adminuser@email.com')
        self.assertEqual(self.admin_user.first_name, 'Admin')
        self.assertEqual(self.admin_user.last_name, 'User')
        self.assertEqual(self.admin_user.entry_tokens, 4)
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)


    
    def test_string_representation(self):
        """
        Test user model string method.
        """

        self.assertEqual(str(self.user), 'Test User')
        self.assertEqual(str(self.admin_user), 'Admin User')


class SignUpCodeTests(TestCase):

    def setUp(self):

        self.signup_code = SignUpCode.objects.create()


    def test_create_signup_code(self):
        """
        Test signup code object creation.
        """
        
        self.assertIsNotNone(self.signup_code.created)
        self.assertIsNotNone(self.signup_code.code)
        self.assertTrue(len(self.signup_code.code)==12)


    def test_string_representation(self):
        """
        Test user signup code string method.
        """

        self.assertEqual(str(self.signup_code), self.signup_code.code)
