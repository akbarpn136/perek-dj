from django.forms import ModelForm, TextInput, SelectMultiple, Textarea, Select
from django import forms

from .models import Kategori, Kegiatan, Format, Personil


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


class FormFormat(ModelForm):
    class Meta:
        model = Format
        exclude = ['format_kegiatan']
        widgets = {
            'format_kegiatan': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_format'}),
            'nama': TextInput(attrs={'placeholder': 'Nama'}),
            'formasi': Textarea(attrs={'rows': '0'}),
        }


class FormPersonil(ModelForm):
    class Meta:
        model = Personil
        exclude = ['personil_kegiatan']
        widgets = {
            'orang': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_orang'}),
            'wbs_wp_pilihan': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_wbs_wp'}),
            'peran': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_peran'}),
            'wbs_wp_nama': TextInput(attrs={'placeholder': 'Nama WBS/WP'}),
            'wbs_wp_kode': TextInput(attrs={'placeholder': 'Kode, misal: 1, 2.1, ...'}),
            'peran_kode': TextInput(attrs={'placeholder': 'Kode, misal: 1, 2.1, ...'}),
            'index': TextInput(attrs={'placeholder': 'Nomor urutan'}),
            'referensi': Textarea(attrs={'rows': '0'}),
        }


class FormMasuk(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
