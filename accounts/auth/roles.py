from django.contrib.auth.models import Group

class UserRole:
    MAHASISWA = "mahasiswa"
    DOSEN = "dosen"
    TU = "tu"
    
def get_user_roles(user):
    return list(
        user.groups.values_list("name", flat=True)
    )
    
def has_role(user, role: str) -> bool:
    return role in get_user_roles(user)