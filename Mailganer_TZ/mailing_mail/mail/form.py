from django import forms


class MailingForm(forms.Form):
    text = forms.CharField(max_length=2 ** 16)
