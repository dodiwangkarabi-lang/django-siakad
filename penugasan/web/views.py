from django.shortcuts import render

# selectors
from academic.selectors.kelas import get_kelas_by_id

def detail_penugasan(request, penugasan_id):
    return render(request, "penugasan/detail-penugasan.html")

def daftar_tugas_by_kelas(request, kelas_id):
    return render(request, "penugasan/daftar-tugas-by-kelas.html")

def daftar_tugas(request):
    return render(request, "penugasan/daftar-tugas.html")

def kirim_tugas(request, penugasan_id):
    context  = {}
    return render(request, "penugasan/kirim-tugas.html", context)