from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils import timezone

from .models import Entry
from . import forms
from . import utils
from .ai import calliopeAI
from core.decorators import require_htmx


@login_required
def entry_list_view(request):
    """
    Lists the current users entries, paginated.
    """
    
    user_entries = Entry.objects.filter(created_by=request.user, deleted=False
        ).order_by('-created_at')

    search_term = request.GET.get('search')
    
    if search_term:
        user_entries = user_entries.filter(messages__body__icontains=search_term).distinct()

    paginator = Paginator(user_entries, 6)
    page = request.GET.get('page')
    user_entries = paginator.get_page(page)

    context = {
        'entry_list': user_entries,
    }
    return render(request, 'entries/entry-list.html', context)


@login_required
def entry_create_redirect_view(request):
    """
    If an entry has not been created today, deducts a token and creates one. 
    If the user doesn't have any tokens, redirects them to the entry limit 
    reached page. Otherwise redirects them to the entry for today.
    """
    
    today = timezone.now().date()
    user = request.user

    # Retrieve existing entry.
    try:
        entry = Entry.objects.get(
            created_by = user,
            created_at__date = today,
        )

    # Create entry and deduct a user token.
    except ObjectDoesNotExist:
        if user.use_entry_token() == True:
            entry = Entry.objects.create(
                created_by = user,
            )
            return redirect(reverse('entry_write'))
        else:
            return redirect(reverse('entries_entry_limit'))

    return redirect(reverse('entry_detail', kwargs={'pk': entry.id}))


@login_required
def entry_detail_view(request, pk):
    """
    Displays a users entry. If the entry created date is equal to today, 
    allow users to add to the entry, otherwise simply show the content.
    """
    
    entry = get_object_or_404(Entry, id=pk)
    entry.created_today = entry.created_at.date() == timezone.now().date()

    context = {
        'entry': entry,
    }

    return render(request, 'entries/entry-detail.html', context)


def entry_write_view(request, pk):

    entry = get_object_or_404(Entry, id=pk)

    if entry.created_at.date() == timezone.now().date():

        form = forms.EntryCreateUpdateForm(instance=entry)

        if request.method == 'POST':
            
            form = forms.EntryCreateUpdateForm(request.POST, instance=entry)
            
            if form.is_valid():
                form.save()
                return redirect('entry_detail', pk=entry.id)
            
        context = {
            'form': form,
            'entry': entry,
        }

        return render(request, 'entries/entry-write.html', context)
    
    else:
        return redirect(reverse('entry_detail', kwargs={'pk': entry.id}))
    

@login_required
def entry_limit_reached_view(request):
    """
    Renders the entry limit reached template, that allows users to upgrade 
    their accounts.
    """
    
    return render(request, 'entries/entry-limit-reached.html')


@login_required
def entry_delete_view(request, pk):

    entry = get_object_or_404(Entry, pk=pk, created_by=request.user)

    if request.method == "POST":
        entry.delete()
        return redirect(reverse('entries_entry_list'))

    context = {
        'entry': entry,
    }

    return render(request, 'entries/delete-entry.html', context)


# @login_required
# @require_htmx
# def entry_message_reply_view(request):
#     """
#     Sends a request to the AI service, bundling the previous messages from 
#     the current entry.
#     """

#     if request.method == 'POST':

#         entry_id = request.POST.get('entry_id')

#         try:
#             entry = Entry.objects.get(id=entry_id, created_by=request.user)
#         except ObjectDoesNotExist:
#             raise Http404
        
#         # Process the messages and send to AI function
#         messages = [
#             {
#                 "role": "assistant" if message.system_reply else "user",
#                 "content": message.body
#             }
#             for message in entry.messages.all()
#         ]

#         response = calliopeAI(messages)
#         message_reply = EntryMessage.objects.create(
#             body = response,
#             entry = entry,
#             system_reply = True,
#         )
        
#         context = {
#             'message': message_reply
#         }

#         return render(request, 'entries/partials/reply-message.html', context)
    
#     else:
#         return PermissionDenied
    

