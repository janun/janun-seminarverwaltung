from django import forms


class ThumbnailFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/thumbnail.html'
