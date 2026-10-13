from rest_framework import serializers

from academic.models import (
    DetailKRS, KRS, Mahasiswa, Kelas, MataKuliah
)

class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = [
            "id",
            "nama",
            "nim",
            "jenis_kelamin",
            "no_hp"
        ]
        
class KRSSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaSerializer(read_only=True)
    
    class Meta:
        model = KRS
        fields = [
            "id",
            "mahasiswa",
            "tahun_ajaran",
            "semester"
        ]

class DetailKRSSerializer(serializers.ModelSerializer):
    krs = KRSSerializer(read_only=True)
    
    class Meta:
        model = DetailKRS
        fields = [
            "id",
            "kelas",
            "krs"
        ]
        
class MataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataKuliah
        fields = [
            "id",
            "nama",
            "sks",
            "semester",
            "kode",
        ]
        
class KelasSerializer(serializers.ModelSerializer):
    mata_kuliah = MataKuliahSerializer(read_only=True)
    
    class Meta:
        model = Kelas
        fields = [
            "id",
            "nama",
            "mata_kuliah"
        ]
        
class DetailKRSKKelasSerializer(serializers.ModelSerializer):
    kelas = KelasSerializer(read_only=True)
    class Meta:
        model = DetailKRS
        fields = [
            "id",
            "kelas",
            "krs"
        ]
        
class KelasforMataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = [
            "id",
            "nama",
        ]
        
class MataKuliahKelasSerializer(serializers.ModelSerializer):
    daftar_kelas = KelasforMataKuliahSerializer(many=True, read_only=True)
    class Meta:
        model = MataKuliah
        fields = [
            "id",
            "nama",
            "sks",
            "semester",
            "kode",
            "daftar_kelas",
        ]
        
class MahasiwaDetailSeriazer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = [
            "id",
            "nama",
            "nim",
            "jenis_kelamin",
            "no_hp"
        ]
        
class KRSMahasiswaPesertaSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiwaDetailSeriazer(read_only=True)
    class Meta:
        model = KRS
        fields = [
            "id",
            "mahasiswa",
            "tahun_ajaran",
            "semester"
        ]

class GabungBanyakKelasRequestSerializer(serializers.Serializer):
    kelas_ids = serializers.ListField(child=serializers.IntegerField())
    mahasiswa_ids = serializers.ListField(child=serializers.IntegerField())
    
class TambahKelasRequestSerializer(serializers.Serializer):
    nama_kelas = serializers.CharField()
    
class GantiNamaKelasRequestSerializer(serializers.Serializer):
    nama_kelas = serializers.CharField()