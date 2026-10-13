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

# ----- service -----
from ...services import services
from ...services.validasiKRS import ValidasiKRS
from ...services.ajukanBanyak import (
    AjukanBanyakService, AjukanBanyakKelasResultDTO, AjukanBanyakKelasParamsDTO
)

class KelasAktif(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Daftar Kelas Aktif",
        responses={
            200: KelasAjukanBanyakSerializer(many=True)
        }
    )
    def get(self, request) -> list[KelasAjukanBanyakSerializer]:
        svc = AjukanBanyakService()
        hasil = svc.daftar_kelas_aktif()
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = KelasAjukanBanyakSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)

class MahasiswaAktif(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Daftar Mahasiswa Aktif",
        responses={
            200: MahasiswaAktifSerializer(many=True)
        }
    )
    def get(self, request) -> list[MahasiswaAktifSerializer]:
        svc = AjukanBanyakService()
        hasil = svc.daftar_mahasiswa_aktif()
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = MahasiswaAktifSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)

class TambahPesertaKelas(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Tambah Peserta Kelas",
        responses={
            200: MahasiswaAjukanBanyakSerializerSerializer(many=True)
        }
    )
    def get(self, request, kelas_id) -> list[MahasiswaAjukanBanyakSerializerSerializer]:
        svc = AjukanBanyakService()
        hasil = svc.daftar_mahasiswa(kelas_id=kelas_id)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = MahasiswaAjukanBanyakSerializerSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)


class DaftarMahasiswaByAngkatan(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Daftar Mahasiswa By Angkatan",
        responses={
            200: MahasiswaAjukanBanyakSerializerSerializer(many=True)
        }
    )
    def get(self, request, angkatan) -> list[MahasiswaAjukanBanyakSerializerSerializer]:
        svc = AjukanBanyakService()
        hasil = svc.daftar_mahasiswa(angkatan=angkatan)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = MahasiswaAjukanBanyakSerializerSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)

class DaftarPesertaKelas(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Daftar Peserta Kelas",
        responses={
            200: MahasiswaAjukanBanyakSerializerSerializer(many=True)
        }
    )
    def get(self, request, kelas_id) -> list[MahasiswaAjukanBanyakSerializerSerializer]:
        dto = AjukanBanyakKelasParamsDTO(
            kelas_ids=[1, 2, 3],
            mahasiswa_ids=[3, 4, 5]
        )
        svc = AjukanBanyakService()
        hasil = svc.daftar_peserta(kelas_id=kelas_id)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = MahasiswaAjukanBanyakSerializerSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)

class DaftarMataKuliahAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Daftar Mata Kuliah dan kelasnya",
        responses={
            200: MataKuliahAjukanBanyakSerializer(many=True)
        }
    )
    def get(self, request) -> list[MataKuliahAjukanBanyakSerializer]:
        dto = AjukanBanyakKelasParamsDTO(
            kelas_ids=[1, 2, 3],
            mahasiswa_ids=[3, 4, 5]
        )
        svc = AjukanBanyakService()
        hasil = svc.daftar_mata_kuliah(periode_krs_id=request.query_params.get("periode_krs_id", 1))
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        hasil_serializer = MataKuliahAjukanBanyakSerializer(instance=hasil.data, many=True)
        
        return Response(data=hasil_serializer.data, status=status.HTTP_200_OK)


class AjukanBanyak(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Ajukah KRS Mahasiswa sekaligus",
        responses={
            200: serializer_response.DetailKRSResponseSerializer(many=True)
        }
    )
    def post(self, request) -> list[serializer_response.DetailKRSResponseSerializer]:
        dto = AjukanBanyakKelasParamsDTO(
            kelas_ids=[1, 2, 3],
            mahasiswa_ids=[3, 4, 5]
        )
        svc = AjukanBanyakService()
        hasil = svc.ajukan_banyak(dto)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        detail_krs_serializer = serializer_response.DetailKRSResponseSerializer(instance=hasil.data, many=True)
        
        return Response(data=detail_krs_serializer.data, status=status.HTTP_200_OK)

class DetailKRSMahasiswaAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Detail KRS Mahasiswa",
        responses={
            200: serializer_response.DetailKRSResponseSerializer(many=True)
        }
    )
    def get(self, request, krs_id) -> list[serializer_response.DetailKRSResponseSerializer]:
        hasil = services.DosenPA.detail_krs_mahasiswa(krs_id=krs_id)
        if not hasil.is_success:
            return Response(data=hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer_response.DetailKRSResponseSerializer(hasil.data, many=True).data)
    
class SetujuiKRSAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Setujui KRS",
    )
    def post(self, request):
        return Response(status=status.HTTP_200_OK)
    
class ValidasiKRSAPIView(APIView):
    # authentication_classes = []
    # permissin_classes = [AllowAny] # untuk izinkan public
    permission_classes = [IsDosen]
    
    @extend_schema(
        tags=["KRS"],
        summary="Validasi KRS",
        request=serializer_request.ValidasiKRSRequestSerializer,
        responses={
            200: "berhasil"
        }
    )
    def post(self, request):
        form_data = serializer_request.ValidasiKRSRequestSerializer(data=request.data)
        if form_data.is_valid():
            data_cleaned = form_data.validated_data
            keterangan = data_cleaned.get("keterangan", "")
            svc = ValidasiKRS()
            hasil = svc.validasi(krs_id=data_cleaned["krs_id"], status=data_cleaned["status"], keterangan=keterangan)
            if hasil.is_success:
                return Response(status=status.HTTP_200_OK, data=hasil.messages)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=hasil.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=form_data.errors)
        
        return Response(status=status.HTTP_400_BAD_REQUEST, data=hasil.errors)
    
class KRSDiajukanAPIView(APIView):
    permission_classes = [IsDosen]
    @extend_schema(
        tags=["KRS"],
        summary="krs yang diajukan mahasiswa",
        responses={
            200: serializer_response.KRSModelSerializer(many=True)
        }
    )
    def get(self, request):
        svc = ValidasiKRS()
        hasil = svc.daftar_krs_diajukan()
        serializer = serializer_response.KRSModelSerializer(hasil.data, many=True)
        return Response(
            status=status.HTTP_200_OK, data=serializer.data
        )