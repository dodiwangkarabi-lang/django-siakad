from accounts import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

import typing

class AuthService:

    # @staticmethod
    # def login(username, password) -> User | None:
    #     try:
    #         user = User.objects.get(username=username)
    #         if user.check_password(password):
    #             return user
    #         else:
    #             return None
    #     except User.DoesNotExist:
    #         return None
        
    @staticmethod
    def login(username, password) -> User | None:
        user = authenticate(username=username, password=password)
        return user
    
    @staticmethod
    def simpan_token(response: Response, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True, 
            secure=False,  # true untuk https (productions)
            samesite="Lax",
            max_age=15 * 60
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True, 
            secure=False,  # true untuk https (productions)
            samesite="Lax",
            max_age=60 * 60 * 24 * 7 * 2, # 2 minggu
        )
        
    @staticmethod
    def hapus_token(response: Response):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token") 
    
    @staticmethod
    def get_current_user(request) -> User | None:
        return request.user
    
    @staticmethod
    def generate_akun(data):
        
        user = User.objects.create_user(**data)
        return user
    
    @staticmethod
    def generate_akun_mahasiswa(daftar_mahasiswa: typing.List[models.Mahasiswa]):
        mahasiswa_list = []
        for data in daftar_mahasiswa:
            # cek apakah user sudah ada
            user_ada = User.objects.filter(username=data.nim).first()
            if user_ada:
                continue
            
            user = User(
                username=data.nim,
                # password=make_password(data.nim)
            )
            user.set_password(data.nim)
            
            mahasiswa_list.append(user)
            
        return mahasiswa_list
        
        
    