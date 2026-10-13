from rest_framework import serializers

from accounts.models import Mahasiswa


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
   
    
    
    
class ProfileMahasiswa(serializers.ModelSerializer): 
    class Meta:
        model = Mahasiswa
        fields = "__all__"