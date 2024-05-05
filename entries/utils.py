import random


def random_initial_message():

    messages = (
        """
        Hello! I'm Calliope, your personal journalling assistant. How can I help you with your daily journal today?
        """,
        """
        Hello! I'm Calliope, here to assist you with your daily journaling. How are you feeling today? Let's start by 
        noting down your thoughts and reflections for the day.
        """,
        """
        Hello! How can I assist you today with your journaling? Are you looking to start your daily journal entry?
        """,
    )

    return random.choices(messages, k=1)[0]