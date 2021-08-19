from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        """Check if url extension is valid"""
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('This image hasn`t jpeg extension')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        # переопределяем метод сохранения, качаем изображение
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # качаем изображение из указанного урл
        page = request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        # обходим ошибку 403 из urllib: открываем ссылку как браузер, а не как python urllib
        resp = request.urlopen(page)
        image.image.save(image_name, ContentFile(resp.read()), save=False)
        if commit:
            image.save()
        return image
