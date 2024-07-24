import calendar

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Entry
from . import forms


@login_required
def entry_list_view(request):
    """
    Lists the current user's entries, paginated and optionally filtered by a 
    search term. Entries are grouped by year and full month name, including 
    detailed entry data.
    """

    search_term = request.GET.get('search')
    
    # Initial query to fetch entries
    base_query = Entry.objects.filter(created_by=request.user, deleted=False
        ).values('pk', 'created_at')
    
    if search_term:
        base_query = base_query.filter(content__icontains=search_term).distinct()

    # Annotate entries with year and month number
    annotated_entries = base_query.annotate(
        year=ExtractYear('created_at'),
        month=ExtractMonth('created_at')
    ).order_by('-year', '-month', '-created_at')

    # Convert month number to month name and group entries by year and month name
    grouped_entries = {}
    for entry in annotated_entries:
        month_name = calendar.month_name[entry['month']]
        year_month = (entry['year'], month_name)
        if year_month not in grouped_entries:
            grouped_entries[year_month] = []
        grouped_entries[year_month].append(entry)

    # Paginate the results based on the filtered and grouped query
    paginator = Paginator(list(grouped_entries.items()), 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'nav_section': 'read',
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

    entry, created = Entry.objects.get_or_create(
        created_by = user,
        created_at__date = today,
    )

    return redirect('entry_write', pk=entry.id)


def entry_write_view(request, pk):

    entry = get_object_or_404(Entry, id=pk)
    form = forms.EntryCreateUpdateForm(instance=entry)

    if request.method == 'POST':
        
        form = forms.EntryCreateUpdateForm(request.POST, instance=entry)
        
        if form.is_valid():
            form.save()
            return redirect('entry_detail', pk=entry.id)
        
    context = {
        'form': form,
        'entry': entry,
        'nav_section': 'write',
    }

    return render(request, 'entries/entry-write.html', context)


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
        'nav_section': 'read',
    }

    return render(request, 'entries/entry-detail.html', context)


@login_required
def entry_limit_reached_view(request):
    """
    Renders the entry limit reached template, that allows users to upgrade 
    their accounts.
    """

    context = {
        'nav_section': 'write',
    }
    
    return render(request, 'entries/entry-limit-reached.html', context)


@login_required
def entry_delete_view(request, pk):

    entry = get_object_or_404(Entry, pk=pk, created_by=request.user)

    if request.method == "POST":
        entry.delete()
        return redirect(reverse('entries_entry_list'))

    context = {
        'entry': entry,
        'nav_section': 'read',
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
    

