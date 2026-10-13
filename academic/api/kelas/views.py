from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict

# doc
from drf_spectacular.utils import extend_schema

from academic.models import Kelas

# serializer
from .serializers import KelasSerializer

# @extend_schema(tags=["kelas"], description="contoh", summary="contohnya")
# class KelasAPIView(APIView):
#     def get(self, request):
#         qs = Kelas.objects.all()
#         serializer = KelasSerializer(qs, many=True)
#         return Response({
#             "success": True,
#             "message": "Berhasil mengambil data",
#             "data": serializer.data
#         })

# def get_kelas_apiview(request):
#     qs = Kelas.objects.all()
#     serializer = KelasSerializer(qs, many=True)
#     return Response({
#         "success": True,
#         "message": "Berhasil mengambil data",
#         "data": serializer.data
#     })

