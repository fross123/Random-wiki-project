import markdown2

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="Search", max_length=64)

class createForm(forms.Form):
    title = forms.CharField(label="title", max_length=64)
    content = forms.CharField(widget=forms.Textarea, label="content")

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": SearchForm()
    })

def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(util.get_entry(title)),
            "search": SearchForm(),
            "title": title

        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "No Entry Found.",
            "search": SearchForm()
        })

def search(request):
    # init empty list of results
    results = []
    form = SearchForm(request.POST)
    if form.is_valid():
        search = form.cleaned_data["search"]

        # if search matches entry, redirect to entry url
        if util.get_entry(search):
            return HttpResponseRedirect(f"wiki/{search}")

        # otherwise create list of matching results with links
        for i in util.list_entries():
            if search.upper() in i.upper():
                results.append(i)

        # if no results in search
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

            # if entry has been made, render error page
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": "This wiki already exists, please try another.",
                    "search": SearchForm()
                })

            # if title does not match current entry, save entry and redirect to new entry
            elif not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(f"wiki/{title}")
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
        if util.get_entry(title):
            form = EditForm(initial={"content": util.get_entry(title)})

            return render(request, "encyclopedia/edit.html", {
                "search": SearchForm(),
                "edit": form,
                "title": title
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "No Entry Found.",
                "search": SearchForm()
            })
    elif request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return entry(request, title)
