import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


# Logging
logger = logging.getLogger('utility_tasks')


def genericSendEmail(template_name, subject, recipients, email_data, task_name=''):
    """
    Send email via template to list of recipients via bcc. Recipients list automatically chunked 
    into batches of 40 email addresses to prevent SMTP overload.

    args:
    template_name (string): Path to template name.
    subject (string): Email subject.
    recipients (list): List of email addresses to which the email will be sent.
    email_data (dict): Context dictionary of data to be utilised within the template.

    kwargs:
    task_name (string): Name of the task, used within logs. 
    """

    logger.info(f'Started task: {task_name}...')
    
    # Load the HTML template using the Django template loader
    html_template = get_template(template_name)

    # Render the template with the context data
    html_content = html_template.render(email_data)

    # Convert to set to remove duplicates & chunk recipients to 40 addresses max
    recipients = list(set(recipients))
    chunked_recipients = [recipients[i:i + 40] for i in range(0, len(recipients), 40)]

    for chunk in chunked_recipients:
        message = EmailMultiAlternatives(
            subject=subject, 
            body='',
            bcc=chunk,
        )
        message.attach_alternative(html_content, 'text/html')
        message.send()

    logger.info(f'Completed task: {task_name}')