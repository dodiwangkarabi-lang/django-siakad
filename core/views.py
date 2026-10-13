from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# models
from accounts.models import Mahasiswa
from academic.models import MataKuliah, Kelas

# forms
from core.forms import FormKRS, FormGabungKelas

# helpers
from academic.helpers.helpers import bulk_krs

from academic.usecases import IsiKRS
from academic.services import (
    DetailKRSService, KelasService, KRSService,
    MataKuliahService
)
from accounts.services import (
    MahasiswaService
)

from academic.helpers.helpers import (
    hitung_total_sks
)

from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, world. You're at the core index.")

def kelas(request):
    return render(request, 'features/krs/pages/kelas.html')

@login_required
def gabung_kelas(request):
    form = FormGabungKelas()
    mahasiswa_qs = Mahasiswa.objects.all().order_by("nama")
    kelas_qs = Kelas.objects.all().order_by("nama")
    if request.method == "POST":
        form_data = request.POST.copy()
        
        data = {
            "tahun_ajaran": form_data.get("tahun_ajaran"),
            "semester": form_data.get("semester"),
            "mahasiswa_ids": form_data.getlist("daftar_mahasiswa[]"),
            "kelas_ids": form_data.getlist("daftar_pilihan_kelas[]"),
        }
        
        # print(data)
        
        objs = bulk_krs(**data)
        # print(objs)
        messages.success(
            request,
            f"Jumlah Data : {len(objs)}"
        )
        
        return redirect("core:gabung_kelas")
    
    context = {
        'form': form,
        'list_kelas': kelas_qs,
        'list_mahasiswa': mahasiswa_qs
    }
    return render(request, 'features/krs/pages/gabung-kelas.html', context)

@login_required
def krs(request):
    mata_kuiah_qs = MataKuliah.objects.all().order_by("nama")
    mahasiswa_qs = Mahasiswa.objects.all().order_by("nama")
    form = FormKRS()
    if request.method == "POST":
        data = request.POST.copy()
        data.setlist('mahasiswa', request.POST.getlist('daftar_nim_mahasiswa[]'))
        list_daftar_pilihan_mata_kuliah = request.POST.getlist('daftar_pilihan_mata_kuliah[]')
    
        data.setlist('daftar_pilihan_mata_kuliah', list_daftar_pilihan_mata_kuliah)
        data["jumlah_sks"] = hitung_total_sks(list_daftar_pilihan_mata_kuliah)
        
        # print(data)
        form = FormKRS(data)
        
        if form.is_valid() and data["jumlah_sks"] <= 24:
            # print(form.cleaned_data)
            # print(dict(form.cleaned_data))
            payload = {
                "daftar_nim": [x.nim for x in form.cleaned_data["mahasiswa"]],
                "daftar_kode_mata_kuliah": [x.kode for x in form.cleaned_data["daftar_pilihan_mata_kuliah"]], #list_daftar_pilihan_mata_kuliah,
                "tahun_ajaran": data["tahun_ajaran"],
                "semester": "genap"
            }
            
            # print(payload)
            # print(data["jumlah_sks"])
            
            uc = IsiKRS(
                krs_service=KRSService(),
                kelas_service=KelasService(),
                mahasiswa_service=MahasiswaService(),
                mata_kuliah_service=MataKuliahService(),
                detail_krs_service=DetailKRSService()
            )
            uc.execute(payload)
            
            messages.success(
                request,
                f"Total SKS : {data['jumlah_sks']}"
            )
            
            return redirect('core:krs')
        else:
            print(form.errors)
        # data = request.POST.list()
        # data = {k: request.POST.getlist(k) for k in request.POST}
        # print(data)
    context = {
        'form': form,
        'list_mata_kuliah': mata_kuiah_qs,
        'list_mahasiswa': mahasiswa_qs
    }
    
    return render(request, 'features/krs/pages/index.html', context)

def submit_krs(request):
    context = {}
    
    return render(request, 'features/krs/pages/index.html', context)