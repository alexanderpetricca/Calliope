from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from .models import Entry, EntryMessage
from . import forms
from .ai import calliopeAI


@login_required
def entryListView(request):
    
    user_entries = Entry.objects.filter(owner=request.user, deleted=False)

    search_term = request.GET.get('search')
    
    if search_term:
        user_entries = user_entries.filter(messages__body__icontains=search_term)

    paginator = Paginator(user_entries, 6)
    page = request.GET.get('page')
    user_entries = paginator.get_page(page)

    context = {
        'entry_list': user_entries,
    }
    return render(request, 'entries/entry-list.html', context)


@login_required
def entryCreateView(request):

    entry = Entry.objects.create(
        owner = request.user
    )

    return redirect(reverse('entries_entry', kwargs={'pk': entry.id}))


@login_required
def entryView(request, pk):
    
    entry = get_object_or_404(Entry, id=pk, owner=request.user)
    form = forms.EntryMessageCreateForm(entry=entry.pk)

    if request.method == 'POST':
        form = forms.EntryMessageCreateForm(request.POST, entry=entry.pk)
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            entry.messages.add(message)

            context = {
                'message': message,
            }

            return render(request, 'entries/partials/entry-message.html', context)


    context = {
        'form': form,
        'entry': entry,
    }

    return render(request, 'entries/entry.html', context)


@login_required
def entryMessageReplyView(request):

    if request.method == 'POST':

        entry_id = request.POST.get('entry_id')

        try:
            entry = Entry.objects.get(id=entry_id, owner=request.user)
        except ObjectDoesNotExist:
            raise Http404
        
        # Process the messages and send to calliopeAI function
        messages = [
            {
                "role": "assistant" if message.system_reply else "user",
                "content": message.body
            }
            for message in entry.messages.all()
        ]

        response = calliopeAI(messages)
        message_reply = EntryMessage.objects.create(
            body = response,
            system_reply = True,
        )
        entry.messages.add(message_reply)
        
        context = {
            'message': message_reply
        }

        return render(request, 'entries/partials/reply-message.html', context)
    
    else:
        return PermissionDenied

