from django.forms import ModelForm, TextInput, Textarea, Select, EmailInput
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
