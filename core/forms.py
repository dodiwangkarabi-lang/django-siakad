from django import forms
from academic.models import Mahasiswa, MataKuliah, Kelas

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
    
class FormGabungKelas(forms.Form):
    daftar_nim_mahasiswa = forms.ModelMultipleChoiceField(
        queryset=Mahasiswa.objects.all(),
        to_field_name='id'
    )
    daftar_kelas = forms.ModelMultipleChoiceField(
        queryset=Kelas.objects.all(),
        to_field_name='id'
    )