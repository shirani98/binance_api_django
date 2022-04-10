from django import forms

class DataForm(forms.Form):
    price = forms.DecimalField()
    symbol = forms.CharField(max_length=10)
    channel_name = forms.CharField(max_length=20, label="Channel Name")

    
    