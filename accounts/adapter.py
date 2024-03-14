from allauth.account.adapter import DefaultAccountAdapter

from environs import Env

# Environs
env = Env()
env.read_env()


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """Extracts environment variable OPEN_FOR_SIGNUP and returns its boolean value."""

        signUpOpen = env("OPEN_FOR_SIGNUP")
        
        if signUpOpen:
            return True
        else:
            return False
