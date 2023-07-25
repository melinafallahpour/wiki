from django.shortcuts import redirect, render
from markdown2 import Markdown
from django.http import HttpResponse
from . import util
from.forms import SearchForm, CreateForm, EditForm
from django.urls import reverse
from django.contrib import messages
import random





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm(),
    })
    

def entry(request, title):
    entry_md = util.get_entry(title)
    if entry_md != None:
        entry_HTML = Markdown().convert(entry_md)
        return render(request, "encyclopedia/entry.html", {
          "title": title,
          "entry": entry_HTML,
          "search_form": SearchForm(),
          })
    else:
        related_titles = util.related_titles(title)
        return render(request, "encyclopedia/error.html", {
          "title": title,
          "related_titles": related_titles,
          "search_form": SearchForm(),
          }) 
        
def search(request):
    if request.method == "POST" :
        form = SearchForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_md = util.get_entry(title)
            
            print('search request : ', title)
            
            if entry_md:
                return redirect (reverse ('entry' , args= [title]))
            else :
                  related_titles = util.related_titles (title)
                  return render (request , "encyclopedia/search.html",{
                    "title" : title , 
                    "related_titles":related_titles,
                    "search_form":SearchForm()
                    })

    return redirect (reverse('index'))



def create(request):
    
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
          "create_form": CreateForm(),
          "search_form": SearchForm()
        })

    elif request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
          title = form.cleaned_data['title']
          text = form.cleaned_data['text']
        else:
          messages.error(request, 'Entry form not valid, please try again!', 'warning')
          return render(request, "encyclopedia/create.html", {
            "create_form": form,
            "search_form": SearchForm()
          })

        if util.get_entry(title):
            messages.error(request, 'This page title already exists! Please go to that title page and edit it instead!','warning')
            return render(request, "encyclopedia/create.html", {
              "create_form": form,
              "search_form": SearchForm()
            })
        else:
            util.save_entry(title, text)
            messages.success(request, f'New page "{title}" created successfully!', 'success')
            return redirect(reverse('entry', args=[title]))


def edit(request, title):

    if request.method == "GET":
        text = util.get_entry(title)

        if text == None:
            messages.error(request, f'"{title}"" page does not exist and can\'t be edited, please create a new page instead!', 'danger')

        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "edit_form": EditForm(initial={'text':text}),
          "search_form": SearchForm()
        })

    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(title, text)
          messages.success(request, f'Article "{title}" updated successfully!', 'success')
          return redirect(reverse('entry', args=[title]))

        else:
          messages.error(request, f'Editing form is not valid, please try again!', 'warning')
          return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": form,
            "search_form": SearchForm()
          })
          
          
          
def random_title(request):


    titles = util.list_entries()
    title = random.choice(titles)

    return redirect(reverse('entry', args=[title]))