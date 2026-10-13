from academic.models import (
    KRS, DetailKRS,
    MataKuliah, Kelas, PenawaranKRS, PeriodeKRS
)

from rest_framework import serializers

# ----- krs -----
class KRSModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KRS
        fields = "__all__"

class ErrorResponseSerializer(serializers.Serializer):
    errors = serializers.DictField()
    
class ListKelasIdsResponseSerializer(serializers.Serializer):
    kelas_ids = serializers.ListField(
        child=serializers.IntegerField()
    )

class KrsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KRS
        fields = "__all__"

class DetailKRSResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailKRS
        fields = "__all__"
        
        
        
# ----- batas -----
class MataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataKuliah
        fields = '__all__'
        
class PeriodeKRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodeKRS
        fields = '__all__'
        
class KelasSerializer(serializers.ModelSerializer):
    mata_kuliah = MataKuliahSerializer(read_only=True)
    class Meta:
        model = Kelas
        fields = '__all__'
        

class PenawaranKRSSerializer(serializers.ModelSerializer):
    periode_krs = PeriodeKRSSerializer()
    kelas = KelasSerializer()
    class Meta:
        model = PenawaranKRS
        fields = '__all__'
        
class KRSDetailKRSResponseSerializer(serializers.ModelSerializer):
    # Kelas = KelasSerializer(source='kelas', read_only=True)
    kelas = KelasSerializer(read_only=True)
    class Meta:
        model = DetailKRS
        fields = "__all__"
        # exclude = ["kelas"]