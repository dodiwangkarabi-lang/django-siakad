from rest_framework import serializers
from academic.models import Kelas, KRS, DetailKRS, MataKuliah, Fakultas, Prodi

class KelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = '__all__'
        
class KRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = KRS
        fields = '__all__'
        
class DetailKRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailKRS
        fields = '__all__'
        
class MataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataKuliah
        fields = '__all__'
        
class FakultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fakultas
        fields = '__all__'
        
class ProdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prodi
        fields = '__all__'