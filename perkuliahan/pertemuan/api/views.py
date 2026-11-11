from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...pertemuan import services
from . import serializers
from .. import dto

# autentifikasi
from rest_framework.permissions import IsAuthenticated
from accounts.auth.permission import (
    IsDosen, IsTU, IsMahasiswa
)

class DaftarHadirPerluKonfirmasiAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def get(self, request, pertemuan_id: int):
        svc = services.KehadiranService()
        result = svc.daftar_hadir_perlu_konfirmasi(user=request.user, pertemuan_id=pertemuan_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ser = serializers.KehadiranDetailSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class IsMahasiswaSudahIsiKehadiran(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    
    def get(self, request, pertemuan_id: int):
        svc = services.KehadiranService()
        result = svc.is_mahasiswa_sudah_isi_kehadiran(user=request.user, pertemuan_id=pertemuan_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # ser = serializers.KehadiranSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": result.data
        }, status=status.HTTP_200_OK)

class KehadiranByKelasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, kelas_id: int):
        svc = services.KehadiranService()
        result = svc.kehadiran_siswa_by_kelas(user=request.user, kelas_id=kelas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ser = serializers.KehadiranSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class KelasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        svc = services.KelasService()
        result = svc.get_kelas(user=request.user)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ser = serializers.KelasSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class PertemuanNilaiTugasAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def post(self, request, kumpul_tugas_id):
        ser = serializers.NilaiTugasSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = ser.validated_data
        data = dto.NilaiTugasDTO(
            nilai=validated_data["nilai"],
            catatan=validated_data.get("catatan", "")
        )
        
        svc = services.TugasService()
        result = svc.nilai_tugas(user=request.user, kumpul_tugas=kumpul_tugas_id, data=data)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": result.messages,
        }, status=status.HTTP_200_OK)
    
    def get(self, request, kumpul_tugas_id):
        svc = services.TugasService()
        result = svc.get_kumpul_tugas_by_id(kumpul_tugas_id=kumpul_tugas_id)
        
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ser = serializers.KumpulanTugasSerializer(instance=result.data, many=False)
        # print(type(result.data))
        # return Response({"test": "berhasil"}, status=status.HTTP_200_OK)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)
        
class PertemuanHapusTugasDikumpulAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, kumpul_tugas_id):
        svc = services.TugasService()
        result = svc.hapus_tugas_dikumpul(kumpul_tugas_id=kumpul_tugas_id, user=request.user)
        
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": result.messages,
        }, status=status.HTTP_200_OK)
    
    

class PertemuanHapusTugasMahasiswaAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def post(self, request, mahasiswa_id, tugas_id):
        svc = services.TugasService()
        result = svc.hapus_tugas_mahasiswa(user=request.user, mahasiswa_id=mahasiswa_id, tugas_id=tugas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": result.messages
        }, status=status.HTTP_204_NO_CONTENT)
        
class TugasDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def post(self, request, tugas_id):
        data = request.data
        ser = serializers.TugasEditSerializer(data=data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = ser.validated_data
        data_dto = dto.EditTugasDTO(
            deadline=validated_data["deadline"],
            bobot=validated_data["bobot"],
            nama=validated_data.get("nama", None),
            url=validated_data.get("url", None),
            by_kehadiran=validated_data["by_kehadiran"]
        )
        
        svc = services.TugasService()
        result = svc.tugas_edit(tugas_id=tugas_id, data=data_dto)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": result.messages
        }, status=status.HTTP_200_OK)

class PertemuanHapusTugasAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def post(self, request, tugas_id):
        svc = services.TugasService()
        result = svc.hapus_tugas(user=request.user, tugas_id=tugas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": result.messages
        }, status=status.HTTP_200_OK)

class PertemuanKirimTugasAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    
    def post(self, request, tugas_id, pertemuan_id):
        ser = serializers.KirimTugasSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = ser.validated_data
        data = dto.KirimTugasDTO(
            url=validated_data.get("url"),
            keterangan=validated_data.get("keterangan"),
            by_kehadiran=validated_data.get("by_kehadiran", False)
        )
        
        svc = services.TugasService()
        result = svc.kirim_tugas(user=request.user, tugas_id=tugas_id ,pertemuan_id=pertemuan_id, data=data)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": result.messages,
            "data": {
                "id": result.data.id,
                "mahasiswa": result.data.mahasiswa.id,
                "tugas": result.data.tugas.id,
                "url": result.data.url,
                "keterangan": result.data.keterangan,
                "created_at": result.data.created_at
            }
        }, status=status.HTTP_201_CREATED)
        
class LihatNilaiTugasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, kelas_id):
        svc = services.NilaiService()
        result = svc.lihat_nilai_tugas(user=request.user, kelas_id=kelas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ser = serializers.KumpulanTugasSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)
        
class HitungPointAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    
    def get(self, request, kelas_id):
        svc = services.NilaiService()
        hasil = svc.hitung_point(user=request.user, kelas_id=kelas_id)
        if not hasil.is_success:
            return Response(hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": hasil.messages,
            "data": hasil.data
        }, status=status.HTTP_200_OK)

class PertemuanSemuaTugasKelasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, kelas_id):
        svc = services.TugasService()
        result = svc.get_tugas_by_kelas(kelas_id=kelas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
            
        ser = serializers.TugasSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class TugasAktifAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    
    def get(self, request):
        svc = services.TugasService()
        result = svc.get_tugas_aktif_by_mahasiswa(user=request.user)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # ser = serializers.TugasSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": result.data
        }, status=status.HTTP_200_OK)
        
class TugasMahasiswaAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    
    def get(self, request):
        svc = services.TugasService()
        result = svc.get_tugas_by_mahasiswa(user=request.user)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # ser = serializers.TugasSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": result.data
        }, status=status.HTTP_200_OK)

class PertemuanAktifAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, kelas_id):
        svc = services.PertemuanServices()
        result = svc.get_pertemuan_aktif(kelas_id=kelas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
            
        ser = serializers.PertemuanSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)
        
class PertemuanSedangBerlangsungAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        svc = services.PertemuanServices()
        result = svc.pertemuan_sedang_berlangsung(user=request.user)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
            
        ser = serializers.PertemuanSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class PertemuanVerifikasiBanyakKehadiranAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def post(self, request, pertemuan_id):
        ser = serializers.VerifikasiBanyakKehadiranSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = ser.validated_data
        data = dto.VerifikasiBanyakKehadiranDTO(
            kehadiran_ids=validated_data["kehadiran_ids"],
            status_verifikasi=dto.StatusVerifikasi(validated_data["status_verifikasi"]),
        )
        svc = services.KehadiranService()
        result = svc.verifikasi_banyak_kehadiran(
            user=request.user,
            pertemuan_id=pertemuan_id,
            data=data
        )
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "messages": result.messages,
        }, status=status.HTTP_200_OK)

class PertemuanDaftarKehadiranMahasiswaAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    
    def get(self, request, pertemuan_id):
        svc = services.KehadiranService()
        result = svc.daftar_kehadiaran_mahasiswa(pertemuan_id=pertemuan_id, user=request.user)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        ser = serializers.KehadiranSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class PertemuanDaftarKehadiranAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def get(self, request, pertemuan_id):
        params = request.query_params
        ser = serializers.FilterKehadiranSerializer(data=params)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = ser.validated_data
        params_dto = dto.FilterKehadiranDTO(
            status_kehadiran=validated_data.get("status_kehadiran"),
            status_verifikasi=validated_data.get("status_verifikasi")
        )
        svc = services.KehadiranService()
        result = svc.daftar_kehadiran(pertemuan_id=pertemuan_id, user=request.user, params=params_dto)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        ser = serializers.KehadiranSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class PertemuanVerifikasiKehadiranAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def post(self, request, kehadiran_id):
        ser = serializers.VerifikasiKehadiranSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = ser.validated_data
        data = dto.VerifikasiKehadiranDTO(
            status_verifikasi=dto.StatusVerifikasi(validated_data["status_verifikasi"]),
        )
        svc = services.KehadiranService()
        result = svc.verifikasi_kehadiran(data=data, user=request.user, kehadiran_id=kehadiran_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            "messages": result.messages
        }, status=status.HTTP_200_OK)

class PertemuanIsiKehadiranAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    
    def post(self, request, pertemuan_id):
        ser = serializers.IsiKehadiranSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = ser.validated_data
        data = dto.PertemuanIsiKehadiranDTO(
            status_kehadiran=dto.StatusKehadiran(validated_data["status_kehadiran"]),
            keterangan=validated_data["keterangan"]
        )
        svc = services.KehadiranService()
        user = request.user
        result = svc.isi_kehadiran(pertemuan_id=pertemuan_id, data=data, user=user)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            "messages": result.messages
        }, status=status.HTTP_200_OK)

class PertemuanTugasDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, tugas_id):
        svc = services.TugasService()
        result = svc.get_by_id(tugas_id=tugas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        ser = serializers.TugasSerializer(instance=result.data, many=False)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)
        
class KumpulanTugasMahasiswaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, tugas_id):
        svc = services.TugasService()
        result = svc.kumpulan_tugas_mahasiswa(tugas_id=tugas_id)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        ser = serializers.KumpulanTugasSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class PertemuanSemuaTugasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pertemuan_id):
        svc = services.TugasService()
        result = svc.get_tugas(pertemuan_id=pertemuan_id)
        ser = serializers.TugasSerializer(instance=result.data, many=True)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)
        
class KelasDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, kelas_id):
        svc = services.KelasService()
        result = svc.kelas_by_id(kelas_id=kelas_id)
        ser = serializers.KelasSerializer(instance=result.data, many=False)
        return Response(data={
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class PertemuanUploadTugasAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    def post(self, request, pertemuan_id):
        ser = serializers.UploadTugasSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = ser.validated_data
        data = dto.UploadTugasDTO(
            deadline=validated_data["deadline"],
            bobot=validated_data["bobot"],
            nama=validated_data["nama"],
            url=validated_data["url"],
            by_kehadiran=validated_data["by_kehadiran"]
        )
        svc = services.TugasService()
        hasil = svc.upload_tugas(pertemuan_id=pertemuan_id, data=data, user=request.user)
        if not hasil.is_success:
            return Response(hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
                "messages": hasil.messages
            }, status=status.HTTP_201_CREATED)

class PertemuanDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pertemuan_id):
        
        svc = services.PertemuanServices()
        result = svc.get_by_id(pertemuan_id=pertemuan_id)
        ser = serializers.PertemuanSerializer(instance=result.data, many=False)
        
        return Response({
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)

class PertemuanAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, kelas_id):
        
        svc = services.PertemuanServices()
        result = svc.get_pertemuan(kelas_id=kelas_id)
        ser = serializers.PertemuanSerializer(instance=result.data, many=True)
        
        return Response({
            "messages": result.messages,
            "data": ser.data
        }, status=status.HTTP_200_OK)
        
class PertemuanDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    def post(self, request, pertemuan_id):
        svc = services.PertemuanServices()
        hasil = svc.delete_by_id(pertemuan_id=pertemuan_id)
        if not hasil.is_success:
            return Response(hasil.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PertemuanCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]
    
    def post(self, request, kelas_id):
        ser = serializers.PertemuanCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = ser.validated_data
        
        data = dto.PertemuanDTO(
            pertemuan_ke=validated_data["pertemuan_ke"],
            nama=validated_data["nama"],
            mulai = validated_data["mulai"],
            selesai = validated_data["selesai"]
        )
        
        svc = services.PertemuanServices()
        result = svc.create_pertemuan(kelas_id=kelas_id, data=data)
        if not result.is_success:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
        # serializer = serializers.PertemuanSerializer(result.data)
        return Response({
            "messages": result.messages
        }, status=status.HTTP_201_CREATED)
        