from django.forms import ModelForm, TextInput

from .models import Kategori, Kegiatan


class FormKategori(ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama']
        widgets = {
            'nama': TextInput(attrs={'placeholder': 'Kategori disini...'})
        }
