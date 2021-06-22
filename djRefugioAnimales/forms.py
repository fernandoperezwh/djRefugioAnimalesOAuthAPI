from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label="Buscador", max_length=50, required=False)