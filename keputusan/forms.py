from django.forms import ModelForm, TextInput, Textarea, Select

from .models import LembarKeputusan


class FormKeputusan(ModelForm):
    class Meta:
        model = LembarKeputusan
        fields = ['nomor', 'tanggal', 'tingkatan', 'uraian', 'isi', 'index', 'pemberi', 'butir']
        widgets = {
            'pemberi': Select(
                attrs={'class': 'ui fluid search dropdown', 'id': 'select_orang'}),
            'tanggal': TextInput(attrs={'placeholder': 'Tanggal pelaksanaan', 'class': 'tanggal'}),
            'butir': TextInput(attrs={'placeholder': 'Nomor butir', 'id': 'butir', 'readonly': 'readonly'}),
            'index': TextInput(attrs={'placeholder': 'Nomor urutan'}),
            'tingkatan': TextInput(attrs={'placeholder': 'Misal: WP1, WBS1.2, ...'}),
            'nomor': Textarea(attrs={'rows': '0', 'id': 'nomor'}),
            'uraian': Textarea(attrs={'rows': '0', 'id': 'uraian'}),
            'isi': Textarea(attrs={'rows': '18', 'id': 'isi'}),
        }
