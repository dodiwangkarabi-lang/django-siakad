from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# extend_schema
from drf_spectacular.utils import extend_schema

from academic.services.krs_service import KRSMahasiswaService
from academic.repository import (
    KRSRepository, MahasiswaRepository
)

from drf_spectacular.utils import extend_schema

# ----- services -----
from academic.krs import services

# ----- serializers -----
from .. import serializers
from ..serializers import serializer_request, serializer_response

class KRSKelasPasarwajoAPIView(APIView):
    # allow any
    authentication_classes = []
    permission_classes = [AllowAny]
    @extend_schema(
        tags=["KRS"],
        summary="KRS Kelas Pasarwajo",
    )
    def get(self, request):
        result = services.Core.krs_kelas_pasarwajo(periode_id=1)
        if not result.is_success:
            return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=result.data, status=status.HTTP_200_OK)

class SemuaKelasAktifAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="Semua kelas aktif",
    )
    def get(self, request, periode_id):
        result = services.Core.kelas_aktif(periode_id)
        if not result.is_success:
            return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        result_serializer = serializer_response.KelasSerializer(result.data, many=True)
        return Response(data=result_serializer.data, status=status.HTTP_200_OK)


class PeriodeKRSAktifAPIView(APIView):
    @extend_schema(
        tags=["KRS"],
        summary="periode krs aktif",
        responses={
            200: serializers.PeriodeKRSSerializer,
        }
    )
    def get(self, request):
        result = services.Core.periode_krs_aktif()
        if result.is_success:
            result_serializer = serializers.PeriodeKRSSerializer(result.data)
            return Response(data=result_serializer.data, status=status.HTTP_200_OK)
        
        return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)


class LihatKRSAktif(APIView):
    @extend_schema(
        summary="Lihat KRS",
        description="Mengirim KRS untuk diproses.",
        parameters=[
            serializers.LihatKRSAktifRequestSerializer
        ],
        responses=serializers.KRSModelSerializer,
        tags=["KRS"],
    )
    def get(self, request):
        data = request.query_params
        serializer_input = serializers.LihatKRSAktifRequestSerializer(data=data)
        is_valid = serializer_input.is_valid()
        if not is_valid:
            return Response(data=serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # uc = KRSMahasiswaService(KRSRepository(), MahasiswaRepository())
        krs_service = KRSMahasiswaService(krs_repo=KRSRepository(), mahasiswa_repo=MahasiswaRepository())
        krs = krs_service.lihat_krs_aktif(
            nim=serializer_input.validated_data["nim"],
            tahun_ajaran=serializer_input.validated_data["tahun_ajaran"],
            semester=serializer_input.validated_data["semester"],
        )
        
        if krs is None:
            return Response({"message": "KRS tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.KRSModelSerializer(krs)
        return Response(serializer.data)