from django import forms
from .models import AdminUsers


class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = AdminUsers
        fields = ('name', 'image',) 