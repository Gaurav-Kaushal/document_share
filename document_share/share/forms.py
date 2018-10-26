from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        widgets = {
            'owner': forms.HiddenInput(),
            'upload_date': forms.HiddenInput(),
        }
        fields = ('file', 'users', 'owner', 'upload_date')
