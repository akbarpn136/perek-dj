from django.forms import ModelForm, TextInput, SelectMultiple, Textarea

from .models import Kategori, Kegiatan


class FormKategori(ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama']
        widgets = {
            'nama': TextInput(attrs={'placeholder': 'Kategori disini...'})
        }


class FormKegiatan(ModelForm):
    class Meta:
        model = Kegiatan
        exclude = ['slug']
        widgets = {
            'kategori_kegiatan': SelectMultiple(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_kategori_multi'}),
            'kapan_dibuat': TextInput(attrs={'class': 'tanggal', 'placeholder': 'Tanggal kegiatan'}),
            'nama': TextInput(attrs={'placeholder': 'Nama'}),
            'kode': TextInput(attrs={'placeholder': 'Kode, misal: APPDev, PERK, ...'}),
            'referensi': Textarea(attrs={'rows': '0'}),
        }
