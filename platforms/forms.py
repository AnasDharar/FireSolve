# app/forms.py
from django import forms

class BulkProblemForm(forms.Form):
    raw_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 30, 'cols': 100}),
    )