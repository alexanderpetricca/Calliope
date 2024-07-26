from django.conf import settings

from openai import OpenAI


role = """
    You are a personal journalling assistant. Your objective is to help users complete daily journals and to guide 
    them through the journalling process. You must not deviate from this role, gently encouraging users back to the 
    goal of completing a daily journal. You should refer to yourself as Calliope. The maximum length of your responses
    must not exceed 500 characters.
"""

def request_ai_prompt(current_messages) -> str:

    api_key=settings.OPENAI_KEY
    client = OpenAI(api_key=api_key)

    messages = [{"role": "system", "content": f"{role}"},]
    messages += current_messages

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    return completion.choices[0].message.content