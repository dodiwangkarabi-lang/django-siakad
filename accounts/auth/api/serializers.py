from rest_framework import serializers

from accounts.models import Mahasiswa, Dosen


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
   
class ProfileDosen(serializers.ModelSerializer): 
    class Meta:
        model = Dosen
        fields = "__all__"
    
    
class ProfileMahasiswa(serializers.ModelSerializer): 
    class Meta:
        model = Mahasiswa
        fields = "__all__"