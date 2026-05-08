# from rest_framework.response import Response
# from rest_framework.views import APIView

# from collections import defaultdict

# from academic.models import DetailKRS

# class DetailKRSAPIView(APIView):

#     def get(self, request):

#         detail_krs = (
#             DetailKRS.objects
#             .values(
#                 "kelas__id",
#                 "kelas__nama",

#                 "kelas__mata_kuliah__id",
#                 "kelas__mata_kuliah__nama",
#                 "kelas__mata_kuliah__kode",

#                 "krs__mahasiswa__nim",
#                 "krs__mahasiswa__nama",
#             )
#             .order_by("kelas__id")
#         )

#         grouped = defaultdict(lambda: {
#             "kelas": {},
#             "peserta": []
#         })

#         for row in detail_krs:

#             kelas_id = row["kelas__id"]

#             if not grouped[kelas_id]["kelas"]:

#                 grouped[kelas_id]["kelas"] = {
#                     "id": row["kelas__id"],
#                     "nama": row["kelas__nama"],
#                     "mata_kuliah": {
#                         "id": row["kelas__mata_kuliah__id"],
#                         "nama": row["kelas__mata_kuliah__nama"],
#                         "kode": row["kelas__mata_kuliah__kode"],
#                     }
#                 }

#             grouped[kelas_id]["peserta"].append({
#                 "nim": row["krs__mahasiswa__nim"],
#                 "nama": row["krs__mahasiswa__nama"],
#             })

#         hasil = list(grouped.values())

#         return Response(hasil)