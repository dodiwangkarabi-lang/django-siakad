from rest_framework import serializers
# from academic.krs.dto.dto import SemesterType
from academic.models import SemesterType

# class KRSModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KRS
#         fields = '__all__'


# ----- mahasiswa: ajukan krs -----
class AjukanKRSRequestSerializer(serializers.Serializer):
    krs_id = serializers.IntegerField()
    

# ----- buat krs request -----
class AddKRSRequestSerializer(serializers.Serializer):
    nim = serializers.CharField()
    tahun_ajaran = serializers.CharField()
    semester = serializers.ChoiceField(choices=SemesterType)

# ----- tambah satu kelas -----
class AddKrsItemRequestSerializer(serializers.Serializer):
    kelas_id = serializers.IntegerField()
    krs_id = serializers.IntegerField()
    

# ----- tambah banyak kelas -----
class TambahBanyakKelasRequestSerializer(serializers.Serializer):
    krs_id = serializers.IntegerField()
    kelas_ids = serializers.ListField(child=serializers.IntegerField())
    
# ----- hapus item dalam krs -----
class RemoveKrsItemRequestSerializer(serializers.Serializer):
    kelas_id = serializers.IntegerField()
    krs_id = serializers.IntegerField()
    
class SaveKrsDraftRequestSerializer(serializers.Serializer):
    kelas_id = serializers.IntegerField()
    
class SubmitKrsRequestSerializer(serializers.Serializer):
    krs_id = serializers.IntegerField()
    
class ValidateKrsRequestSerializer(serializers.Serializer):
    krs_id = serializers.IntegerField()
    
# ----- validasi krs -----
class ValidasiKRSRequestSerializer(serializers.Serializer):
    status = serializers.CharField()
    keterangan = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    krs_id = serializers.IntegerField()