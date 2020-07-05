import markdown2

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from random import choices

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="Search", max_length=64)

class createForm(forms.Form):
    title = forms.CharField(label="title", max_length=64)
    content = forms.CharField(widget=forms.Textarea, label="")

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": SearchForm()
    })

def entry(request, title):
    # if entry matches title
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title)),
            "search": SearchForm(),
            "title": title

        })
    # entry does not exist
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "No Entry Found.",
            "search": SearchForm()
        })

def search(request):
    # empty list of results
    results = []
    form = SearchForm(request.POST)
    if form.is_valid():
        search = form.cleaned_data["search"]

        # if search matches entry, redirect to entry
        if util.get_entry(search):
            return HttpResponseRedirect(f"wiki/{search}")

        # append matching results to results list
        for i in util.list_entries():
            if search.upper() in i.upper():
                results.append(i)

        # no results from search entry
        if not len(results):
            return render(request, "encyclopedia/error.html", {
                "error": "No results for search.",
                "search": SearchForm()
            })

        # display results of search
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": results,
                "search": SearchForm()
            })

    # search is invalid
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "Invalid Search.",
            "search": SearchForm()
        })

def new(request):
    if request.method == "POST":
        form = createForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # entry exisits, render error page
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": "This wiki already exists, please try another.",
                    "search": SearchForm()
                })

            # title does not match current entry, save entry and redirect to the new entry
            elif not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(f"wiki/{title}")

        # form submission not valid
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "Invalid Submission.",
                "search": SearchForm()
            })

    elif request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "search": SearchForm(),
            "create": createForm()
        })

def edit(request, title):
    if request.method == "GET":
        # entry exisits
        if util.get_entry(title):
            # populate form with current content
            form = EditForm(initial={"content": util.get_entry(title)})

            return render(request, "encyclopedia/edit.html", {
                "search": SearchForm(),
                "edit": form,
                "title": title
            })
        # enry does not exist
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "No Entry Found. Please create a new one.",
                "search": SearchForm()
            })
    elif request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]

            # save the updated entry, redirect to entry
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")

def random(request):
    # pick a random choice from list
    x = choices(util.list_entries())

    # list to a str
    y = "".join(x)

    # redirect to wiki page
    return HttpResponseRedirect(f"/wiki/{y}")
