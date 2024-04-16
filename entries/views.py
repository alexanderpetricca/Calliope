from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils import timezone

from .models import Entry, EntryMessage
from . import forms
from .ai import calliopeAI
from core.decorators import require_htmx


@login_required
def appHomeView(request):
    user_entries = Entry.objects.filter(owner=request.user, deleted=False)

    paginator = Paginator(user_entries, 6)
    page = request.GET.get('page')
    user_entries = paginator.get_page(page)

    context = {
        'entry_list': user_entries,
    }
    return render(request, 'entries/home.html', context)



@login_required
@require_htmx
def entryListView(request):
    
    user_entries = Entry.objects.filter(owner=request.user, deleted=False)

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
@require_htmx
def entryCreateRedirectView(request):
    
    today = timezone.now().date()
    user = request.user

    # Retrieve existing entry.
    try:
        entry = Entry.objects.get(
            owner = user,
            created__date = today,
        )

    # Create entry and deduct a user token.
    except ObjectDoesNotExist:
        if user.useToken() == True:
            entry = Entry.objects.create(
                owner = user,
            )
        else:
            return redirect(reverse('entries_entry_limit'))

    return redirect(reverse('entries_entry', kwargs={'pk': entry.id}))


@login_required
@require_htmx
def entryView(request, pk):
    
    entry = get_object_or_404(Entry, id=pk, owner=request.user)
    today = timezone.now().date()

    # If entry was not created today, do not render form.
    if entry.created.date() == today:

        form = forms.EntryMessageCreateForm()

        if request.method == 'POST':
            form = forms.EntryMessageCreateForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.entry = entry
                message.save()

                context = {
                    'message': message,
                }
                return render(request, 'entries/partials/entry-message.html', context)
            
    else:
        form = None

    context = {
        'form': form,
        'entry': entry,
    }
    return render(request, 'entries/entry.html', context)


@login_required
@require_htmx
def entryMessageReplyView(request):

    if request.method == 'POST':

        entry_id = request.POST.get('entry_id')

        try:
            entry = Entry.objects.get(id=entry_id, owner=request.user)
        except ObjectDoesNotExist:
            raise Http404
        
        # Process the messages and send to AI function
        messages = [
            {
                "role": "assistant" if message.system_reply else "user",
                "content": message.body
            }
            for message in entry.entrymessage_set.all()
        ]

        response = calliopeAI(messages)
        message_reply = EntryMessage.objects.create(
            body = response,
            entry = entry,
            system_reply = True,
        )
        
        context = {
            'message': message_reply
        }

        return render(request, 'entries/partials/reply-message.html', context)
    
    else:
        return PermissionDenied
    

@login_required
@require_htmx
def entryDeleteView(request, pk):

    entry = get_object_or_404(Entry, pk=pk, owner=request.user)

    if request.method == "POST":
        entry.delete()
        return redirect(reverse('entries_entry_list'))

    context = {
        'entry': entry,
    }

    return render(request, 'entries/delete-entry.html', context)


@login_required
def entryLimitReachedView(request):
    
    return render(request, 'entries/entry-limit-reached.html')