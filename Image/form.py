from django.forms import ModelForm

from Image.models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']
