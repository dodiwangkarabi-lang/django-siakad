from rest_framework import permissions

class IsMahasiswa(permissions.BasePermission):
    message = "Anda tidak di izinkan untuk melakukan aksi ini"
    def has_permission(self, request, view):
        return request.user.groups.filter(name="mahasiswa").exists()
    
class IsDosen(permissions.BasePermission):
    message = "Anda tidak di izinkan untuk melakukan aksi ini"
    def has_permission(self, request, view):
        return request.user.groups.filter(name="dosen").exists()
    
class IsTU(permissions.BasePermission):
    message = "Anda tidak di izinkan untuk melakukan aksi ini"
    def has_permission(self, request, view):
        return request.user.groups.filter(name="tu").exists()