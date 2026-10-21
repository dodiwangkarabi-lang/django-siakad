from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone

import random
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
# status
from rest_framework import status

from .services import KelasSlotService, dto
from .selectors import selectors
from . import serializers

# auth
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.auth.permission import (
    IsDosen, IsTU, IsMahasiswa
)

class HapusDosenPengampuAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTU]
    
    @extend_schema(
        tags=["Kelola_Kelas"],
        summary="hapus dosen pengampu",
        responses={
            200: {"success": True, "message": "Berhasil hapus dosen pengampu"}
        },
        
    )
    def post(self, request, kelas_id):
        
        hasil = KelasSlotService.hapus_dosen_pengampu(kelas_id=kelas_id)
        if not hasil.is_success:
            return Response({"success": False, "message": "Terjadi Kesalahan"})
        return Response({"success": True, "message": "Berhasil", "data": None})


class SetDosenPengampuAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTU]
    
    @extend_schema(
        tags=["Kelola_Kelas"],
        summary="set dosen pengampu",
        responses={
            200: {"success": True, "message": "Berhasil mengambil data"}
        },
        request=serializers.SetDosenPengampuidRequestSerializer
    )
    def post(self, request, kelas_id):
        data = {
            "kelas_id": kelas_id,
            "dosen_id": request.data["dosen_id"]
        }
        ser = serializers.SetDosenPengampuRequestSerializer(data=data)
        if not ser.is_valid():
            return Response({"success": False, "message": "Terjadi Kesalahan"})
        
        data_dto = dto.SetDosenPengampuRequeestDTO(**ser.validated_data) 
        hasil = KelasSlotService.set_dosen_pengampu(dto=data_dto)
        if not hasil.is_success:
            return Response({"success": False, "message": "Terjadi Kesalahan"})
        return Response({"success": True, "message": "Berhasil", "data": ser.data})

class DosenPengampuAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTU]
    
    @extend_schema(
        tags=["Kelola_Kelas"],
        summary="dosen pengampu",
        responses={
            200: {"success": True, "message": "Berhasil mengambil data"}
        },
    )
    def get(self, request):
        qs = selectors.dosen_list()
        ser = serializers.DosenModelSerializer(instance=qs, many=True)
        return Response({"success": True, "message": "Berhasil mengambil data", "data": ser.data})
    
    @extend_schema(
        tags=["Kelola_Kelas"],
        summary="tambah dosen pengampu",
        responses={
            200: {"success": True, "message": "Berhasil", "data": serializers.DosenModelSerializer}
        },
        request=serializers.DosenPengampuTambahSerializer
    )
    def post(self, request):
        random_nip = random.randint(1000000000, 9999999999)
        mydata = {
            "nama": request.data["nama"],
            "nip": request.data.get("nip", random_nip),
            "no_hp": request.data.get("no_hp", "")
        }
        ser = serializers.DosenPengampuTambahSerializer(data=mydata)
        if not ser.is_valid():
            print(ser.errors)
            return Response({"success": False, "message": "Terjadi Kesalahan"}, status=status.HTTP_400_BAD_REQUEST)
        
        data_dto = dto.DosenPengampuTambahDTO(**ser.validated_data) 
        hasil = KelasSlotService.tambah_dosen_pengampu(dto=data_dto)
        if not hasil.is_success:
            return Response({"success": False, "message": "Terjadi Kesalahan"}, status=status.HTTP_400_BAD_REQUEST)
        dosen_serializer = serializers.DosenModelSerializer(instance=hasil.data)
        return Response({"success": True, "message": "Berhasil tambah data", "data": dosen_serializer.data})

class KelasListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTU]
    
    @extend_schema(
        tags=["Kelola_Kelas"],
        summary="kelas list",
        responses={
            200: {"success": True, "message": "Berhasil mengambil data"}
        },
    )
    def get(self, request):
        kelas_qs = selectors.kelas_list()
        ser = serializers.KelasModelSerializer(instance=kelas_qs, many=True)
        return Response({"success": True, "message": "Berhasil mengambil data", "data": ser.data})

class DownloadJadwalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTU]
    
    @extend_schema(
        tags=["Kelola_Kelas"],
        summary="download jadwal",
        responses={
            200: {"success": True, "message": "Berhasil mengambil data"}
        },
        request=serializers.DownloadJadwalRequestSerializer(many=True)
    )
    def post(self, request):
        ser = serializers.DownloadJadwalRequestSerializer(data=request.data, many=True)
        if not ser.is_valid():
            return Response({"success": False, "message": "Gagal mengambil data"})
        data = ser.validated_data
        # print(data)
        template_path = settings.MEDIA_ROOT / "template_excel" / "template_jadwal.xlsx"
        hasil = KelasSlotService.download(template_jadwal=template_path, kelas_slot_selected=data)
        if not hasil.is_success:
            return Response({"success": False, "message": "Gagal mengambil data"})
        
        buffer = hasil.data
        now = timezone.localtime()
        filename = f"JADWAL {now:%d-%m-%Y_%H-%M}.xlsx"
        
        response = HttpResponse(buffer, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

class JadwalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTU]
    
    @extend_schema(
        tags=["Kelola_Kelas"],
        summary="Detail KRS Mahasiswa",
        responses={
            200: {"success": True, "message": "Berhasil mengambil data"}
        }
    )
    def get(self, request):
        hasil = KelasSlotService.get_slot()
        if not hasil.is_success:
            return Response({"success": False, "message": "Gagal mengambil data"})
        
        isi_slot_request = {
            "field": "C15",
            "kelas_id": 130
        }
        return Response({"success": True, "message": "Berhasil mengambil data", "data": hasil.data})