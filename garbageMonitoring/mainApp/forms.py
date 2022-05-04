from django import forms
from .models import garbageLog

class DataEntryForm(forms.ModelForm):
    class Meta:
        model = garbageLog
        fields = ("ratio",)