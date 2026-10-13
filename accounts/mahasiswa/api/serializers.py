from rest_framework import serializers
from accounts.models import Mahasiswa

class BiodataMahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        exclude = ['user']