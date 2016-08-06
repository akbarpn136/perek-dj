from django.forms import ModelForm, TextInput, Textarea, Select
# from django import forms

from .models import *


class FormLI(ModelForm):
    class Meta:
        model = LembarInstruksi
        exclude = ['nama', 'kegiatan', 'pemberi', 'angka', 'kesepakatan']
        widgets = {
            'penerima': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_orang'}),
            'tanggal': TextInput(attrs={'placeholder': 'Tanggal pelaksanaan', 'class': 'tanggal'}),
            'butir': TextInput(attrs={'placeholder': 'Nomor butir', 'id': 'butir', 'readonly': 'readonly'}),
            'index': TextInput(attrs={'placeholder': 'Nomor urutan'}),
            'nomor': Textarea(attrs={'rows': '0', 'id': 'nomor'}),
            'referensi': Textarea(attrs={'rows': '0', 'id': 'referensi'}),
            'isi': Textarea(attrs={'rows': '18', 'id': 'isi'}),
        }


class FormKesepakatan(ModelForm):
    class Meta:
        model = LembarInstruksi
        fields = ['kesepakatan']
