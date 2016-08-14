from django.forms import ModelForm, TextInput, Textarea, Select
# from django import forms

from .models import *


class FormLB(ModelForm):
    class Meta:
        model = Logbook
        exclude = ['nama', 'kegiatan', 'angka', 'li', 'penerima']
        widgets = {
            'pemeriksa': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_orang_pemeriksa'}),
            'pemberi': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_orang'}),
            'referensi': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_referensi'}),
            'tanggal': TextInput(attrs={'placeholder': 'Tanggal pelaksanaan', 'class': 'tanggal'}),
            'butir': TextInput(attrs={'placeholder': 'Nomor butir', 'id': 'butir', 'readonly': 'readonly'}),
            'index': TextInput(attrs={'placeholder': 'Nomor urutan'}),
            'nomor': Textarea(attrs={'rows': '0', 'id': 'nomor'}),
            'isi': Textarea(attrs={'rows': '18', 'id': 'isi'}),
        }