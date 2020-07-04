import markdown

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": SearchForm()
    })

def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(util.get_entry(title)),
            "search": SearchForm()

        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "No Entry Found.",
            "search": SearchForm()
        })

def search(request):
    results = []
    form = SearchForm(request.POST)
    if form.is_valid():
        search = form.cleaned_data["search"]
        if util.get_entry(search):
            return HttpResponseRedirect(f"entry/{search}")
        for i in util.list_entries():
            if search.upper() in i.upper():
                results.append(i)
        return render(request, "encyclopedia/search.html", {
            "entries": results,
            "search": SearchForm()
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "error": "Invalid Search.",
            "search": SearchForm()
        })
