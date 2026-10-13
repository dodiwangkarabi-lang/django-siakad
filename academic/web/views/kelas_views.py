from django.shortcuts import render, redirect

# selectors
from academic.selectors.kelas import get_kelas_by_id

def daftar_materi(request):
    return render(request, 'materi/daftar-materi.html')

def daftar_kelas(request):
    return render(request, 'kelas/daftar-kelas.html')

def kelas(request):
    return render(request, 'features/krs/pages/kelas.html')

def detail_kelas(request, kelas_id):
    kelas = get_kelas_by_id(kelas_id)
    context = {
        "kelas": kelas
    }
    return render(request, 'kelas/detail-kelas.html', context)