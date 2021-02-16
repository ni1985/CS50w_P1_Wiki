import markdown2
import random
import re

from django import forms
from django.shortcuts import render

from . import util

#class Search_Query(forms.Form):
#    search_query = forms.CharField(label="search_query", max_length=50)

class New_Entry(forms.Form):
    entry_title = forms.CharField(label="Title", max_length=25)
    entry_text = forms.CharField(label="Markdown text", widget=forms.Textarea(attrs={"rows":5, "cols":20}))

class Edit_Entry(forms.Form):
    edit_text = forms.CharField(label="Markdown text", widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    title = forms.CharField(widget=forms.HiddenInput())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_page):

    ls_entries = util.list_entries() 
    #for i in range(0, len(ls_entries)):
    #    ls_entries[i] = ls_entries[i].lower()

    if entry_page in ls_entries: 

        # Convert markdown text into HTML using the markdown module
        text = markdown2.markdown(util.get_entry(entry_page))

        return render(request, "encyclopedia/entry.html", {
            "entry_text": text,
            "entry_page": entry_page.lower()
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f"The entry \"{entry_page}\" was not found"
        })

def search(request):

    if request.method == "POST":
        query = request.POST.get('q')
        search_result = []
        ls_entries = util.list_entries()    

        for i in range(0, len(ls_entries)):
            if query.lower() == ls_entries[i].lower():
                search_result.append(ls_entries[i])
                print(ls_entries[i])    
        
        if search_result: 
            return render(request, "encyclopedia/search.html", {
                "search_result": search_result,
                "query": query,
                "search_n": 1
            })
        
        else:
            for e in ls_entries:
                if re.search(query.lower(), e.lower()):
                    search_result.append(e)
                    print(f"append {e}")
        
        search_n = len(search_result)
        return render(request, "encyclopedia/search.html", {
            "search_result": search_result,
            "query": query,
            "search_n": search_n
        })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def new_page(request):

    if request.method == "POST":
        
        form = New_Entry(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            ls_entries = util.list_entries()    

            for i in range(0, len(ls_entries)):
                if entry_title.lower() == ls_entries[i].lower():
                    search_result.append(ls_entries[i])
                    print(f"duplication: {ls_entries[i]}")    
                    
                    return render(request, "encyclopedia/error.html", {
                        "message": f"Entry \"{ls_entries[i]}\" already exists"
                    })

            entry_text = form.cleaned_data["entry_text"]
            util.save_entry(entry_title, entry_text)
        
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": New_Entry()
        })

def rnd(request):
    
    length = len(util.list_entries())
    rnd = random.randint(0, length-1)
    
    entry_page = util.list_entries()[rnd]
    text = markdown2.markdown(util.get_entry(entry_page))

    return render(request, "encyclopedia/entry.html", {
        "entry_text": text,
        "entry_page": entry_page.capitalize()
    })

def edit(request):

    if request.method == "POST":
        form = Edit_Entry(request.POST)
        print(form)

        if form.is_valid():
            edit_text = form.cleaned_data["edit_text"]
            edit_title = form.cleaned_data["title"]
            ls_entries = util.list_entries()

            for i in range(0, len(ls_entries)):
                print(ls_entries[i])
                if edit_title.lower() in ls_entries[i].lower():
                    print('yes')
                    util.save_entry(ls_entries[i], edit_text)
                    

                    print(ls_entries[i])
                    print(edit_text)
                    
                    return render(request, "encyclopedia/entry.html", {
                        "entry_text": ls_entries[i],
                        "entry_page": edit_text
                    })
                
                else:
                    return render(request, "encyclopedia/error.html", {
                            "message": f"Entry \"{edit_title}\" not found"
                        })

    else:
        edit_title = request.GET#('edit')
        print(f"title of the entry is {edit_title['edit']}")


        entry = util.get_entry(edit_title['edit'])
        print(f"initial entry text is {entry}")
        
        form = Edit_Entry(initial={'edit_text': entry, 'title': edit_title['edit']})

        return render(request, "encyclopedia/edit_page.html", {
            "form": form,
            "title": edit_title['edit']
        })
