from django import forms


class ThumbnailFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/thumbnail.html'

    def __init__(self, *args, **kwargs):
        self.logo = kwargs.pop('logo', False)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['logo'] = self.logo
        # print(context)
        return context