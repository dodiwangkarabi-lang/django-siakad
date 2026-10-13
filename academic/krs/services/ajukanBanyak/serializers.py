from academic.models import (
    MataKuliah, Kelas, Mahasiswa
)

from rest_framework import serializers

class MahasiswaAktifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = [
            "id",
            "nama",
            "nim"
        ]

class KelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = [
            "id",
            "nama",
            # "kode",
            # "waktu",
            # "ruangan",
        ]
        

class MataKuliahAjukanBanyakSerializer(serializers.ModelSerializer):
    daftar_kelas = KelasSerializer(many=True, read_only=True)
    class Meta:
        model = MataKuliah
        fields =  [
            "id", "nama", "sks", "kode", "semester", "jenis",
            "daftar_kelas", 
        ]
        
class KelasAjukanBanyakSerializer(serializers.ModelSerializer):
    daftar_kelas = KelasSerializer(many=True, read_only=True)
    class Meta:
        model = MataKuliah
        fields =  [
            "id", "nama", "sks", "kode", "semester", "jenis",
            "daftar_kelas", 
        ]
        
class MahasiswaAjukanBanyakSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = [
            "id",
            "nama",
            "nim", 
            "no_hp",
            "jenis_kelamin"
        ]
