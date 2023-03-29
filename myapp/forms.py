from django import forms

class JsonFileUploadForm(forms.Form):
    json_file = forms.FileField(
        label='Upload JSON file',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'formFile', 'style': 'width: 300px;'})
    )
