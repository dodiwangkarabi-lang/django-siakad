from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# extend_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter

from . import serializers
from .. import services

class SemuaNimAPIView(APIView):
    @extend_schema(tags=["Mahasiswa"], summary="Semua NIM")
    def get(self, request):
        result = services.MahasiswaService.getNimNamaList()
        if not result.is_success:
            return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK, data=result.data)

class BiodataMahasiswaAPIView(APIView):
    @extend_schema(
        tags=["Mahasiswa"], summary="Biodata Mahasiswa",
        responses=serializers.BiodataMahasiswaSerializer,
        parameters=[
            OpenApiParameter(
                name="nim",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="NIM Mahasiswa"
            ),
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="ID Mahasiswa"
            ),
        ]
    )
    def get(self, request):
        nim = request.query_params.get("nim", None)
        mahasiswa_id = request.query_params.get("id", None)
        
        if nim:
            result = services.MahasiswaService.biodata(nim=nim)
            if not result.is_success:
                return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)
            mhs_sz = serializers.BiodataMahasiswaSerializer(result.data)
            return Response(status=status.HTTP_200_OK, data=mhs_sz.data)
        
        if mahasiswa_id:
            result = services.MahasiswaService.biodata(id=mahasiswa_id)
            if not result.is_success:
                return Response(data=result.errors, status=status.HTTP_400_BAD_REQUEST)
            mhs_sz = serializers.BiodataMahasiswaSerializer(result.data)
            return Response(status=status.HTTP_200_OK, data=mhs_sz.data)
        
        return Response(data={"non_field_errors": ["nim atau id harus diisi"]}, status=status.HTTP_400_BAD_REQUEST)