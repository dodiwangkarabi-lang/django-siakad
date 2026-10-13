from academic.models import Kelas

from rest_framework import serializers

class KelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = '__all__'