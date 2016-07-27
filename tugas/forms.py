from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput
# from django import forms

from .models import *


class Form(ModelForm):
    class Meta:
        model = LembarInstruksi
        exclude = ['nama', 'kegiatan', 'pemberi', 'angka']
        widgets = {
            'penerima': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_orang'}),
            'tanggal': TextInput(attrs={'placeholder': 'Tanggal pelaksanaan'}),
            'butir': TextInput(attrs={'placeholder': 'Nomor butir'}),
            'index': TextInput(attrs={'placeholder': 'Nomor urutan'}),
            'nomor': Textarea(attrs={'rows': '0', 'id': 'nomor'}),
            'referensi': Textarea(attrs={'rows': '0', 'id': 'referensi'}),
            'isi': Textarea(attrs={'rows': '0', 'id': 'isi'}),
        }
