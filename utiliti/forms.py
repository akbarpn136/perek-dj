from django.forms import ModelForm, TextInput, Textarea, Select, EmailInput
from django import forms
from django.contrib.auth.models import User

from .models import Profil


class FormPersonil(ModelForm):
    class Meta:
        model = Profil
        exclude = ['user']
        widgets = {
            'nip': TextInput(attrs={'placeholder': 'NIP'}),
            'pendidikan': TextInput(attrs={'placeholder': 'Misal: S1/Teknik'}),
            'instansi': Textarea(attrs={'rows': '0'}),
            'instansi_kode': TextInput(attrs={'placeholder': 'Misal: BUK'}),
            'jabatan': TextInput(attrs={'placeholder': 'Misal: Staff'}),
            'pangkat': Textarea(attrs={'rows': '0'}),
            'jenjang': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_jenjang'}),
        }


class FormUser(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Misal: Fulan'}),
            'last_name': TextInput(attrs={'placeholder': 'Misal: Fulan, ST'}),
            'email': EmailInput(attrs={'placeholder': 'Misal: contoh@contoh.com'}),
        }


class FormGantiSandi(forms.Form):
    password_lama = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password lama'}),
                                    label='Password Lama')
    password_baru = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password baru'}),
                                    label='Password Baru')
    password_konfirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'konfirmasi password'}),
                                       label='Konfirmasi Password')
