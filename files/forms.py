from django import forms
from .models import Directory


class UploadFileForm(forms.Form):

    file = forms.FileField()


class DirectoryForm(forms.ModelForm):

    class Meta:
        model = Directory
        fields = ['dir_name', 'description']