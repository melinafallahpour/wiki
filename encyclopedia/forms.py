from cProfile import label
from turtle import title
from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label= '' ,widget=forms.TextInput(attrs={
        "class" : "search" , 
        "placeholder":"search wikipedia"
        
    }))


class CreateForm(forms.Form):
  
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Article Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Article Content"
    }))
    
    
class EditForm(forms.Form):
      
  text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))