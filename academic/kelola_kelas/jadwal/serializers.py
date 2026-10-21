from rest_framework import serializers
from academic.models import (
    Kelas, MataKuliah
)
from accounts.models import (
    Dosen
)

class SetDosenPengampuRequestSerializer(serializers.Serializer):
    kelas_id = serializers.IntegerField()
    dosen_id = serializers.IntegerField()
    
class SetDosenPengampuidRequestSerializer(serializers.Serializer):
    dosen_id = serializers.IntegerField()

class DownloadJadwalRequestSerializer(serializers.Serializer):
    kelas_id = serializers.IntegerField()
    field = serializers.CharField()
    
class MataKuliahModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataKuliah
        fields = '__all__'
        
class DosenModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        # fields = '__all__'
        exclude = ['created_at', 'updated_at', "user"]
        
class DosenPengampuTambahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = ["nama", "nip", "no_hp"]
    
class KelasModelSerializer(serializers.ModelSerializer):
    mata_kuliah = MataKuliahModelSerializer(read_only=True)
    dosen = DosenModelSerializer(read_only=True)
    
    # methodfield
    total_mahasiswa = serializers.IntegerField(read_only=True)
    class Meta:
        model = Kelas
        fields = '__all__'
        
    # def get_total_mahasiswa(self, obj):
    #     return obj.total_mahasiswa
    