from django.shortcuts import render
from accounts.models import Dosen, Mahasiswa
from django.contrib.auth.models import User
from accounts.serializers import (
    DosenSerializer, MahasiswaSerializer, UserSerializer
)
from rest_framework.viewsets import ModelViewSet

class DosenViewSet(ModelViewSet):
    queryset = Dosen.objects.all()
    serializer_class = DosenSerializer
    
class MahasiswaViewSet(ModelViewSet):
    queryset = Mahasiswa.objects.all()
    serializer_class = MahasiswaSerializer
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
