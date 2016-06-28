from django.forms import ModelForm, TextInput, SelectMultiple, Textarea, Select
from django import forms

from .models import *


class Form(ModelForm):
    class Meta:
        model = ''
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
