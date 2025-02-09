from django import forms


class CreateThreadForm(forms.Form):
    title = forms.CharField(max_length=255)
    caption = forms.CharField(widget=forms.Textarea)