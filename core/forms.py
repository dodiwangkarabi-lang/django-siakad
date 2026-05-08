from django import forms
from academic.models import Mahasiswa, MataKuliah

class FormKRS(forms.Form):
    jumlah_sks = forms.CharField()
    mahasiswa = forms.ModelMultipleChoiceField(
        queryset=Mahasiswa.objects.all(),
        to_field_name='nim'
    )
    daftar_pilihan_mata_kuliah = forms.ModelMultipleChoiceField(
        queryset=MataKuliah.objects.all(),
        to_field_name='kode'
    )