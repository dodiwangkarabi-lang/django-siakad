from academic.models import DetailKRS, KRS
from academic import models
from rest_framework import serializers

class DetailKRSModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailKRS
        fields = '__all__'
        
class KRSModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KRS
        fields = '__all__'
        
class LihatKRSAktifRequestSerializer(serializers.Serializer):
    nim = serializers.CharField()
    tahun_ajaran = serializers.CharField()
    semester = serializers.CharField()
    
# ----- input -----

class MataKuliahResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nama = serializers.CharField()
    kode = serializers.CharField()


class KelasResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nama = serializers.CharField()
    mata_kuliah = MataKuliahResponseSerializer()


class PesertaKRSResponseSerializer(serializers.Serializer):
    nim = serializers.CharField()
    nama = serializers.CharField()


class DetailKRSResponseSerializer(serializers.Serializer):
    kelas = KelasResponseSerializer()
    peserta = PesertaKRSResponseSerializer(many=True)
    

class PeriodeKRSSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.PeriodeKRS
        fields = "__all__"