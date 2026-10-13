from django.conf import settings

from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# ----- permission -----
from accounts.auth.permission import IsDosen, IsTU, IsMahasiswa
from accounts.auth.authentication import CookieJWTAuthentication
from rest_framework.permissions import AllowAny

# ----- serializer -----
from ..serializers import serializer_response
from ..serializers import serializer_request

# ----- serializer ajukan banyak -----
from ...services.ajukanBanyak.serializers import (
    MataKuliahAjukanBanyakSerializer, MahasiswaAjukanBanyakSerializerSerializer,
    MahasiswaAktifSerializer, KelasSerializer,
    KelasAjukanBanyakSerializer
)
# ----- lihat daftar krs -----
from ...services.lihatDaftarKRS.serializers import (
    MahasiswaSerializer, DetailKRSKKelasSerializer,
    KRSSerializer, MataKuliahKelasSerializer,
    KRSMahasiswaPesertaSerializer,
    GabungBanyakKelasRequestSerializer,
    TambahKelasRequestSerializer,
    GantiNamaKelasRequestSerializer
)

# ----- service -----
from ...services import services
from ...services.validasiKRS import ValidasiKRS
from ...services.ajukanBanyak import (
    AjukanBanyakService, AjukanBanyakKelasResultDTO, AjukanBanyakKelasParamsDTO
)
from ...services.lihatDaftarKRS import (
    LihatDaftarKRS, KelaService
)

from academic.krs.services.daftarHadir.daftarHadirService import (
    ExcelService, Query
)
# timezone
from django.utils import timezone
from django.http import HttpResponse

class DownloadDaftarHadir(APIView):
    @extend_schema(tags=["KRS"], summary="Download Daftar Hadir")
    def get(self, request, kelas_id):
        
        # kelas_id = 130
        template_path = settings.MEDIA_ROOT / "krs" / "template" / "DAFTAR_HADIR_TEMPLATE.xlsx"
        dosen_nama = "Dodiman, S.Kom., M.Kom."
        dosen_nidn = "0928079403"
        hasil = ExcelService.excecute(
            kelas_id=kelas_id, template_path=template_path,
            DOSEN_PEMBINA=dosen_nama,
            NIDN=dosen_nidn
        )
        # hasil.data
        
        file_bytes = hasil.data

        now = timezone.localtime()
        filename = f"DAFTAR HADIR {now:%d-%m-%Y_%H-%M}.xlsx"

        response = HttpResponse(file_bytes, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

class GantiNamaKelasAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Tambah Kelas",
        request=GantiNamaKelasRequestSerializer,
        responses={
            200: {"message": "success"}
        }
    )
    def post(self, request, kelas_id):
        # validasi data input
        ser = GantiNamaKelasRequestSerializer(data=request.data)
        if not ser.is_valid():
            return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            validated_data = ser.validated_data
            
        svc = KelaService()
        hasil = svc.ganti_nama(kelas_id=kelas_id, nama_kelas=validated_data["nama_kelas"])
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # hasil_serializer = KRSMahasiswaPesertaSerializer(instance=hasil.data, many=True)
        
        return Response(data={"message": "success"}, status=status.HTTP_200_OK)


class HapusKelasAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Hapus Kelas",
        responses={
            200: {"message": "success"}
        }
    )
    def post(self, request, kelas_id):
        # validasi data input
            
        svc = KelaService()
        hasil = svc.hapus_kelas(kelas_id=kelas_id)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # hasil_serializer = KRSMahasiswaPesertaSerializer(instance=hasil.data, many=True)
        
        return Response(data={"message": "success"}, status=status.HTTP_200_OK)

class TambahKelasAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Tambah Kelas",
        request=TambahKelasRequestSerializer,
        responses={
            200: {"message": "success"}
        }
    )
    def post(self, request, mata_kuliah_id):
        # validasi data input
        ser = TambahKelasRequestSerializer(data=request.data)
        if not ser.is_valid():
            return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            validated_data = ser.validated_data
            
        svc = KelaService()
        hasil = svc.tambah_kelas(mata_kuliah_id=mata_kuliah_id, nama_kelas=validated_data["nama_kelas"])
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # hasil_serializer = KRSMahasiswaPesertaSerializer(instance=hasil.data, many=True)
        
        return Response(data={"message": "success"}, status=status.HTTP_200_OK)

class GabungBanyakKelasAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Daftar KRS Peserta",
        request=GabungBanyakKelasRequestSerializer,
        responses={
            200: {"message": "success"}
        }
    )
    def post(self, request):
        # validasi data input
        ser = GabungBanyakKelasRequestSerializer(data=request.data)
        if not ser.is_valid():
            return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            validated_data = ser.validated_data
            
        svc = KelaService()
        hasil = svc.gabung_banyak_kelas(kelas_ids=validated_data["kelas_ids"], mahasiswa_ids=validated_data["mahasiswa_ids"])
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # hasil_serializer = KRSMahasiswaPesertaSerializer(instance=hasil.data, many=True)
        
        return Response(data={"message": "success"}, status=status.HTTP_200_OK)

class KRSPesertaAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Daftar KRS Peserta",
        responses={
            200: KRSMahasiswaPesertaSerializer(many=True)
        }
    )
    def get(self, request, kelas_id) -> list[KRSMahasiswaPesertaSerializer]:
        svc = LihatDaftarKRS()
        hasil = svc.peserta_kelas(kelas_id=kelas_id)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = KRSMahasiswaPesertaSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)
    
class PenawaranMataKuliahKelasAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Mata Kuliah beserta Daftar kelasnya",
        responses={
            200: MataKuliahKelasSerializer(many=True)
        }
    )
    def get(self, request) -> list[MataKuliahKelasSerializer]:
        svc = LihatDaftarKRS()
        hasil = svc.penawaran_mata_kuliah_kelas
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = MataKuliahKelasSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)

class MataKuliahKelasAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Mata Kuliah beserta Daftar kelasnya",
        responses={
            200: MataKuliahKelasSerializer(many=True)
        }
    )
    def get(self, request) -> list[MataKuliahKelasSerializer]:
        svc = LihatDaftarKRS()
        hasil = svc.mata_kuliah_kelas
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = MataKuliahKelasSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)

class DetailKRS(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Detail KRS",
        responses={
            200: DetailKRSKKelasSerializer(many=True)
        }
    )
    def get(self, request, krs_id) -> list[DetailKRSKKelasSerializer]:
        svc = LihatDaftarKRS()
        hasil = svc.detail_krs(krs_id=krs_id)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = DetailKRSKKelasSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)

class MahasiswaKRSSelesaiAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Mahasiswa Selesai KRS",
        responses={
            200: KRSSerializer(many=True)
        }
    )
    def get(self, request) -> list[KRSSerializer]:
        svc = LihatDaftarKRS()
        hasil = svc.krs
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = KRSSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)