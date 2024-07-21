import requests
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from entries.models import Entry

from environs import Env


# Creates test entries for use in development.
# $ python manage.py runscript create-test-entries

# Environs
env = Env()
env.read_env()


def run():

    debug = env.bool("DJANGO_DEBUG", default=False)

    if debug:

        # Request lorem ipsum from loripsum.net API
        try:
            lorem = requests.get('https://loripsum.net/api/10/plaintext/')
        except ConnectionError as e:
            print('API connection error:')
            print(e)
            pass
        
        # Set default date difference value, and get the 'first' user
        date_difference = 0
        author = get_user_model().objects.first()

        for i in range(0, 300):
            created_datetime = timezone.now() - timedelta(days=date_difference)

            new_entry = Entry.objects.create(
                created_by = author,
                content = lorem.text,
            )
            new_entry.created_at = created_datetime
            new_entry.save()

            print(f'Created new entry: {new_entry.id}')

            date_difference += 1

    else:
        print('Debug == True, operation aborted.')
