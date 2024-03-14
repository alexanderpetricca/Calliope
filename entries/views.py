from django.shortcuts import get_object_or_404, render

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Entry
from . import forms


@login_required
def appHomeView(request):
    user_entries = Entry.objects.filter(author=request.user, deleted=False)

    paginator = Paginator(user_entries, 6)
    page = request.GET.get('page')
    user_entries = paginator.get_page(page)

    context = {
        'entry_list': user_entries,
    }
    return render(request, 'entries/home.html', context)


@login_required
def entryListView(request):
    
    user_entries = Entry.objects.filter(author=request.user, deleted=False)

    paginator = Paginator(user_entries, 6)
    page = request.GET.get('page')
    user_entries = paginator.get_page(page)

    context = {
        'entry_list': user_entries,
    }
    return render(request, 'entries/entry-list.html', context)


@login_required
def entryDetailView(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if entry.author == request.user:
        context = {
            'entry': entry,
        }
        return render(request, 'entries/entry-detail.html', context)
    else:
        raise PermissionDenied()


@login_required
def entryCreateView(request):

    form = forms.EntryCreateForm()

    if request.method == 'POST':
        form = forms.EntryCreateForm(request.POST, user=request.user)
        
        if form.is_valid():
            new_entry = form.save()

            return HttpResponseRedirect(reverse('entries:entry_detail', args=[new_entry.id]))

    context = {
        'form': form
    }

    return render(request, 'entries/entry-create.html', context)


@login_required
def entryUpdateView(request, pk):
    
    entry = get_object_or_404(Entry, pk=pk)

    if entry.author == request.user:

        form = forms.EntryUpdateForm(instance=entry)

        if request.method == 'POST':
            form = forms.EntryUpdateForm(request.POST, instance=entry)
                
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('entries:entry_detail', args=[entry.id]))

        context = {
            'form': form, 
            'entry': entry 
            }

        return render(request, 'entries/entry-update.html', context)
    
    else:
        raise PermissionDenied()


def entryDeleteView(request, pk):

    entry = get_object_or_404(Entry, pk=pk)

    if request.method == "POST" and entry.author == request.user:
        entry.softDelete()
        messages.add_message(request, messages.SUCCESS, 'Entry Deleted')
        return HttpResponseRedirect(reverse('entries:entry_list'))

    else:
        raise PermissionDenied()
    

@login_required
def toggleBookmarkView(request, pk):
    
    entry = Entry.objects.get(id=pk)

    if request.method == 'POST':
        entry.bookmark()

    return HttpResponseRedirect(reverse('entries:entry_detail', args=[entry.id]))
