from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

# from rest_framework_simplejwt.tokens import RefreshToken    

from drf_spectacular.utils import extend_schema

from accounts.auth.utils import roles

from .. import services
from . import serializers

class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Auth"], summary="Me")
    def get(self, request):
        
        profile_serializer = serializers.ProfileMahasiswa(request.user.mahasiswa)
        
        return Response({
            "is_success": True,
            "data": {
                "id": request.user.id,
                "username": request.user.username,
                "role": roles.get_role(request),
                "profile": profile_serializer.data
            }
        }, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    @extend_schema(
        tags=["Auth"], summary="Login",
        request=serializers.LoginRequestSerializer
    )
    def post(self, request):
        
        serializer = serializers.LoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        
        user = services.AuthService.login(username=username, password=password)
        if user is None:
            return Response(data={"non_field_errors": ["username atau password salah"]}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({
            "is_success": True,
            "message": "Login berhasil",
        }, status=status.HTTP_200_OK)
        
        services.AuthService.simpan_token(response=response, user=user)
        
        return response
    
class LogoutAPIView(APIView):
    @extend_schema(tags=["Auth"], summary="Logout")
    def post(self, request):
        response = Response({
            "is_success": True,
        }, status=status.HTTP_200_OK)
        services.AuthService.hapus_token(response=response)
        return response