from django.shortcuts import render
from academic.models import KRS, DetailKRS, Kelas, MataKuliah, Prodi, Fakultas
from academic.serializers import (
    KRSSerializer, DetailKRSSerializer, KelasSerializer,
    MataKuliahSerializer, ProdiSerializer, FakultasSerializer
)

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# uath restframework
from rest_framework.permissions import IsAuthenticated
from collections import defaultdict

# ----- serializer -----
from academic.krs.api.serializers import (
    DetailKRSResponseSerializer
)

class FakultasView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Fakultas.objects.all()
    serializer_class = FakultasSerializer
    
class ProdiView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Prodi.objects.all()
    serializer_class = ProdiSerializer
    
class MataKuliahView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = MataKuliah.objects.all()
    serializer_class = MataKuliahSerializer
    
class KelasView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Kelas.objects.all()
    serializer_class = KelasSerializer
    
class DetailKRSView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = DetailKRS.objects.all()
    serializer_class = DetailKRSSerializer
    
class KRSView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = KRS.objects.all()
    serializer_class = KRSSerializer
    

@extend_schema(tags=["KRS"], responses=DetailKRSResponseSerializer)
class DetailKRSAPIView(APIView):

    def get(self, request):

        detail_krs = (
            DetailKRS.objects
            .values(
                "kelas__id",
                "kelas__nama",

                "kelas__mata_kuliah__id",
                "kelas__mata_kuliah__nama",
                "kelas__mata_kuliah__kode",

                "krs__mahasiswa__nim",
                "krs__mahasiswa__nama",
            )
            .order_by(
                "kelas__mata_kuliah__nama",
                "kelas__nama",
                "krs__mahasiswa__nim"
            )
        )

        grouped = defaultdict(lambda: {
            "kelas": {},
            "peserta": []
        })

        for row in detail_krs:

            kelas_id = row["kelas__id"]

            if not grouped[kelas_id]["kelas"]:

                grouped[kelas_id]["kelas"] = {
                    "id": row["kelas__id"],
                    "nama": row["kelas__nama"],
                    "mata_kuliah": {
                        "id": row["kelas__mata_kuliah__id"],
                        "nama": row["kelas__mata_kuliah__nama"],
                        "kode": row["kelas__mata_kuliah__kode"],
                    }
                }

            grouped[kelas_id]["peserta"].append({
                "nim": row["krs__mahasiswa__nim"],
                "nama": row["krs__mahasiswa__nama"],
            })

        hasil = list(grouped.values())

        return Response(hasil)
