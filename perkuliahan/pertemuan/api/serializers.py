from rest_framework import serializers

from academic.models import (
    MataKuliah
)
from perkuliahan.pertemuan.dto import StatusVerifikasi
from ...models import (
    Pertemuan, Kelas, Tugas, StatusKehadiran, StatusVerifikasiKehadiran, Kehadiran,
    Mahasiswa, KumpulTugas, Nilai
)

class MataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataKuliah
        fields = '__all__'
        
class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        # fields = '__all__'
        exclude=['user']

class KelasSerializer(serializers.ModelSerializer):
    mata_kuliah = MataKuliahSerializer(read_only=True)
    class Meta:
        model = Kelas
        fields = '__all__'

class PertemuanCreateSerializer(serializers.Serializer):
    pertemuan_ke = serializers.IntegerField()
    nama = serializers.CharField()
    mulai = serializers.DateTimeField()
    selesai = serializers.DateTimeField()

class PertemuanSerializer(serializers.ModelSerializer):
    kelas = KelasSerializer(read_only=True)
    class Meta:
        model = Pertemuan
        fields = '__all__'
        
class PertemuanOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pertemuan
        fields = '__all__'
        
        
class UploadTugasSerializer(serializers.Serializer):
    deadline = serializers.DateTimeField()
    bobot = serializers.IntegerField()
    nama = serializers.CharField()
    url = serializers.CharField()
    by_kehadiran = serializers.BooleanField(default=False)
    
class TugasEditSerializer(serializers.Serializer):
    deadline = serializers.DateTimeField()
    bobot = serializers.IntegerField()
    nama = serializers.CharField()
    url = serializers.CharField()
    by_kehadiran = serializers.BooleanField(default=False)
    
class TugasSerializer(serializers.ModelSerializer):
    # pertemuan = PertemuanSerializer(read_only=True)
    class Meta:
        model = Tugas
        fields = '__all__'
        # exclude=['pertemuan']
        
class IsiKehadiranSerializer(serializers.Serializer):
    status_kehadiran = serializers.ChoiceField(
        choices=StatusKehadiran.choices
    )
    keterangan = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
class VerifikasiKehadiranSerializer(serializers.Serializer):
    status_verifikasi = serializers.ChoiceField(
        choices=StatusVerifikasiKehadiran.choices
    )
    
class VerifikasiBanyakKehadiranSerializer(serializers.Serializer):
    status_verifikasi = serializers.ChoiceField(
        choices=StatusVerifikasiKehadiran.choices
    )
    kehadiran_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )
    
class KehadiranSerializer(serializers.ModelSerializer):
    pertemuan = PertemuanOnlySerializer(read_only=True)
    mahasiswa = MahasiswaSerializer(read_only=True)
    class Meta:
        model = Kehadiran
        fields = '__all__'

class KehadiranDetailSerializer(serializers.ModelSerializer):
    pertemuan = PertemuanOnlySerializer(read_only=True)
    mahasiswa = MahasiswaSerializer(read_only=True)
    class Meta:
        model = Kehadiran
        fields = '__all__'         

class KirimTugasSerializer(serializers.Serializer):
    url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    keterangan = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    by_kehadiran = serializers.BooleanField(default=False)
    
class NilaiTugasModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nilai
        fields = '__all__'
    
class NilaiTugasSerializer(serializers.Serializer):
    nilai = serializers.IntegerField()
    catatan = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
class FilterKehadiranSerializer(serializers.Serializer):
    status_kehadiran = serializers.ChoiceField(
        choices=StatusKehadiran.choices,
        required=False
    )
    status_verifikasi = serializers.ChoiceField(
        choices=StatusVerifikasiKehadiran.choices,
        required=False
    )
    
class NilaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nilai
        # fields = '__all__'
        exclude=['kumpul_tugas']
    
class KumpulanTugasSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaSerializer(read_only=True)
    tugas = TugasSerializer(read_only=True)
    nilai = NilaiSerializer(read_only=True)
    class Meta:
        model = KumpulTugas
        fields = '__all__'