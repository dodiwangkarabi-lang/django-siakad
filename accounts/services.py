from accounts.models import Dosen, Mahasiswa
from django.contrib.auth.models import User
from django.db import transaction
from shared.services import BaseModelService

def get_user_by_email(email):
    try:
        return Dosen.objects.get(user__email=email)
    except Dosen.DoesNotExist:
        return Mahasiswa.objects.get(user__email=email)
    except Mahasiswa.DoesNotExist:
        return User.objects.get(email=email)
    
    return None

def get_user_by_id(user_id):
    try:
        return Dosen.objects.get(user__id=user_id)
    except Dosen.DoesNotExist:
        return Mahasiswa.objects.get(user__id=user_id)
    except Mahasiswa.DoesNotExist:
        return User.objects.get(id=user_id)
    
    return None

def get_user_by_username(username):
    try:
        return Dosen.objects.get(user__username=username)
    except Dosen.DoesNotExist:
        return Mahasiswa.objects.get(user__username=username)
    except Mahasiswa.DoesNotExist:
        return User.objects.get(username=username)
    
    return None

class MahasiswaService(BaseModelService):
    model = Mahasiswa
    
class DosenService(BaseModelService):
    model = Dosen

# class MahasiswaService:
    
#     @staticmethod
#     def get_all_update_fields():
#         exclude = ["id", "nim", "created_at"]
#         return [
#             field.name
#             for field in Mahasiswa._meta.fields
#             if field.name not in exclude
#         ]
    
#     @staticmethod
#     @transaction.atomic
#     def bulk_save(data_list):
#         """keterangan

#         Args:
#             data_list (list): Array Dict
#                 contoh: [
#                     {
#                         "nama": "nama",
#                         "nim": "nim",
#                         "jurusan": "jurusan"
#                     }
#                 ]
#         """
#         objs = [
#             Mahasiswa(**data)
#             for data in data_list
#         ]
        
#         return Mahasiswa.objects.bulk_create(
#             objs,
#             update_conflicts=True,
#             unique_fields=["nim"], # penentu bentrok
#             # update_fields=["status", "prodi"], # field yang diupdate
#             update_fields=MahasiswaService.get_all_update_fields(),
#             batch_size=1000
#         )