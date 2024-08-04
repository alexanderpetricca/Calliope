from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AccountsViewTests(TestCase):

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
        

    # Login ----

    def test_login_view_logged_out(self):
        """
        Tests the login page is returned when the user is logged out.
        """

        self.client.logout()
        
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_login_view_logged_in(self):
        """
        Tests the user is redirected when the user accesses the login page, 
        when already logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
      

    # Signup ----

    # Password Reset ----

    # Profile Page ----

    def test_user_profile_view_logged_out(self):
        """
        Tests if user is redirected to login when signed out, whilst trying to 
        access the profile page.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/accounts/profile/")
        
        response = self.client.get(f"{reverse('login')}?next=/accounts/profile/")
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Calliope | Login')


    def test_user_profile_view_logged_in(self):
        """
        Tests the profile page is returned when user is logged in.
        """

        self.client.login(email="testuser@email.com", password="testpass123")  
        
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'Calliope | Profile')


    # Update Profile ----
    
    # Update Email ----
    
    # Update Logout ----