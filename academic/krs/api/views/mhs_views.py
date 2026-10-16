from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from django.utils import timezone

from academic.services.krs_service import KRSMahasiswaService
from academic.repository import KRSRepository, MahasiswaRepository

from academic.models import KRS, DetailKRS, PeriodeKRS
from accounts.models import TandaTangan

# ----- permission -----
from accounts.auth.permission import IsMahasiswa, IsDosen
from accounts.auth.roles import has_role

# ----- serializer -----
from ..serializers import serializer_request as sr
from ..serializers import serializer_request as serializer_req
from ..serializers import serializer_response as serializer_res

# ----- service -----
from academic.krs import services
from academic.krs.services.cetakService import CetakService

# ----- dto -----
from ...dto import mhs_dto
from ...dto import dto
from academic.krs.services.cetakService.dto import KRSValues


# ----- lihat kelas yang dipilih (berdasarkan krs id) -----
class KelasDipilihAPIView(APIView):
    permission_classes = [IsMahasiswa | IsDosen]
    # permission_classes = [IsMahasiswa]
    @extend_schema(
        tags=["KRS"],
        summary="Kelas yang dipilih",
        responses=serializer_res.KRSDetailKRSResponseSerializer,
    )
    def get(self, request, krs_id):
        krs = KRS.objects.filter(id=krs_id).first()
        if krs is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # cek pemilik krs
        is_pemilik = krs.mahasiswa.user == request.user
        if not is_pemilik:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "Anda bukan pemilik krs ini"})

        list_obj = DetailKRS.objects.select_related(
            "kelas", "kelas__mata_kuliah"
        ).filter(krs=krs)
        if not list_obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializer_res.KRSDetailKRSResponseSerializer(list_obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# ----- krs mahasiswa -----
class KRSSayaAPIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="tahun_ajaran",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Tahun Ajaran",
            ),
            OpenApiParameter(
                name="semester",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Semesterj, misal: Ganjil, Genap",
            ),
            OpenApiParameter(
                name="nim",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="NIM Mahasiswa",
            ),
        ],
        tags=["KRS"],
        summary="KRS Saya",
        responses=serializer_res.ListKelasIdsResponseSerializer,
    )
    def get(self, request):
        result = services.Mhs.krs_saya(
            nim=request.query_params.get("nim", None),
            tahun_ajaran=request.query_params.get("tahun_ajaran", None),
            semester_type=request.query_params.get("semester", None),
        )
        if not result.is_success:
            return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)

        # data = [0, 1, ]
        ser = serializer_res.ListKelasIdsResponseSerializer({"kelas_ids": result.data})
        return Response(status=status.HTTP_200_OK, data=ser.data)


class KRSMahasiswaAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="KRS Mahasiswa",
        parameters=[
            OpenApiParameter(
                name="tahun_ajaran",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Tahun Ajaran",
            ),
            OpenApiParameter(
                name="semester",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Semesterj, misal: Ganjil, Genap",
            ),
            OpenApiParameter(
                name="krs_id",
                type=int,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID KRS",
            ),
        ],
    )
    def get(self, request, krs_id):
        result = services.Mhs.krs_mahasiswa(
            krs_id=krs_id,
            tahun_ajaran=request.query_params.get("tahun_ajaran", None),
            semester_type=request.query_params.get("semester", None),
        )
        if not result.is_success:
            return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK, data=result.data)


class PenarawanKRSAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Penarawan KRS",
        parameters=[
            OpenApiParameter(
                name="semester_level",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Semester level: 1, 2, dst",
            )
        ],
        responses={
            200: serializer_res.PenawaranKRSSerializer,
            400: serializer_res.ErrorResponseSerializer,
        },
    )
    def get(self, request, periode_id):
        semester_level = request.query_params.get("semester_level", 0)
        semester_level = int(semester_level)
        svc = services.Core.penawaran_krs(
            periode_id=periode_id, semester_level=semester_level
        )

        seriazer = serializer_res.PenawaranKRSSerializer(svc.data, many=True)
        return Response(seriazer.data, status=status.HTTP_200_OK)


class AjukanKRSAPIView(APIView):
    permission_classes = [IsMahasiswa]

    @extend_schema(
        tags=["KRS"],
        summary="Mahasiswa Ajukan KRS",
        request=serializer_req.AjukanKRSRequestSerializer,
        responses={200: "berhasil", 400: "errors"},
    )
    def post(self, request):
        serializer = serializer_req.AjukanKRSRequestSerializer(data=request.data)
        if serializer.is_valid():
            data_cleaned = serializer.validated_data

            # cek apakah user (mahasiswa) adalah pemilik
            is_mahasiswa = has_role(request.user, "mahasiswa")
            if is_mahasiswa:
                mahasiswa = request.user.mahasiswa
                hasil = services.Mhs.ajukan_krs(
                    krs_id=data_cleaned["krs_id"], mahasiswa_id=mahasiswa.id
                )
            else:
                hasil = services.Mhs.ajukan_krs(krs_id=data_cleaned["krs_id"])

            if hasil.is_success:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=hasil.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class CetakKRSAPIView(APIView):
    @extend_schema(tags=["KRS"], summary="Cetak KRS")
    def get(self, request, krs_id):
        try:
            krs = KRS.objects.get(id=krs_id)
        except KRS.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        periode_krs = PeriodeKRS.objects.filter(
            semester=krs.semester, tahun_ajaran=krs.tahun_ajaran
        ).first()
        if periode_krs is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cetak_svc = CetakService()
        cetak_svc.open_pdf(periode_krs.template.path)
        cetak_svc.load_meta_doc(
            periode_krs.template_meta_field.path, sheet_name="meta_doc"
        )

        # mata kuliah yang dipilih
        kode_mata_kuliah_list = DetailKRS.objects.filter(krs=krs).values_list(
            "kelas__mata_kuliah__kode", flat=True
        )
        kode_mata_kuliah_dict = {
            kode_mata_kuliah: "check.png" for kode_mata_kuliah in kode_mata_kuliah_list
        }
        
        # tanda_tangan_img = TandaTangan.objects.filter(user=krs.mahasiswa.user).first()
        tanda_tangan_img = TandaTangan.objects.filter(
            user__mahasiswa__krs__id=krs_id
        ).first()
        
        total_sks = services.Core.hitung_total_sks(krs_id=krs_id)

        DATA_INPUT: KRSValues = {
            **kode_mata_kuliah_dict,
            "NIM": krs.mahasiswa.nim,
            "NAMA_MAHASISWA": krs.mahasiswa.nama,
            "TTL": f"{krs.mahasiswa.tempat_lahir}, {krs.mahasiswa.tanggal_lahir.strftime('%d-%m-%Y')}",
            "NO_HP": f"{krs.mahasiswa.no_hp}",
            "TTD_NAMA": f"{krs.mahasiswa.nama}",
            "TTD_NIM": f"{krs.mahasiswa.nim}",
            "JUMLAH_SKS": f"{total_sks}",
            # "TANGGAL_PENGISIAN": f"{timezone.now().strftime('%d-%m-%Y')}",
            "TANGGAL_PENGISIAN": f"Sabtu, 10 Oktober 2026",
            "TTD_MAHASISWA": tanda_tangan_img.tanda_tangan.path,
        }
        cetak_svc.set_data_input(DATA_INPUT)
        # cetak_svc.load_data_input(periode_krs.template_meta_field.path, sheet_name="value")
        file_bytes = cetak_svc.cetak

        now = timezone.localtime()
        filename = f"KRS_{krs.mahasiswa.nim}_{krs.tahun_ajaran}_{krs.semester} {now:%d-%m-%Y_%H-%M}.pdf"

        response = HttpResponse(file_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class BuatKRSAPIView(APIView):
    @extend_schema(
        request=sr.AddKRSRequestSerializer,
        responses={
            400: serializer_res.ErrorResponseSerializer
        },
        tags=["KRS"],
        summary="Buat KRS Baru atau Update KRS",
    )
    def post(self, request):
        serializer_request = sr.AddKRSRequestSerializer(data=request.data)
        if serializer_request.is_valid():
            # ----- service -----
            service = services.Mhs()
            dto = mhs_dto.BuatKrs(**serializer_request.validated_data)
            result = service.buat_atau_update(dto)
            if result.is_success:
                return Response(status=status.HTTP_201_CREATED, data={"krs_id": result.data})
            return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data=serializer_request.errors, status=status.HTTP_400_BAD_REQUEST
        )


class HapusItemKRSAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Hapus item KRS",
        description="Hapus Kelas dari KRS",
        request=sr.RemoveKrsItemRequestSerializer,
        responses={400: serializer_res.ErrorResponseSerializer, 204: None},
    )
    def post(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)


class TambahBanyakKelasAPIView(APIView):
    permission_classes = [IsMahasiswa]

    @extend_schema(
        tags=["KRS"],
        summary="Tambah Banyak Kelas ke KRS",
        request=sr.TambahBanyakKelasRequestSerializer,
        responses={400: serializer_res.ErrorResponseSerializer},
    )
    def post(self, request):
        serializer = sr.TambahBanyakKelasRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = mhs_dto.TambahBanyakKelas(**serializer.validated_data)
        result = services.Mhs.tambah_banyak_kelas(dto, user=request.user)
        if not result.is_success:
            return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class TambahKelasAPIView(APIView):
    @extend_schema(
        summary="Tambah Kelas ke KRS",
        request=sr.AddKrsItemRequestSerializer,
        tags=["KRS"],
        responses={400: serializer_res.ErrorResponseSerializer},
    )
    def post(self, request):
        serializer_request = sr.AddKrsItemRequestSerializer(data=request.data)
        if serializer_request.is_valid():
            # ----- service -----
            service = services.Mhs()
            dto = mhs_dto.TambahKelas(**serializer_request.validated_data)
            result = service.tambah_kelas(dto)

            if not result.is_success:
                return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)

        return Response(
            data=serializer_request.errors, status=status.HTTP_400_BAD_REQUEST
        )
