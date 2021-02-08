import markdown2

from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_page):

    if entry_page in util.list_entries(): 

        # Convert markdown text into HTML using the markdown module
        text = markdown2.markdown(util.get_entry(entry_page))

        return render(request, "encyclopedia/entry.html", {
            "entry_text": text,
            "entry_page": entry_page.capitalize()
        })
    
    else:
        return render(request, "encyclopedia/not_found.html")

def search(request):
    return render(request, "encyclopedia/search.html")
