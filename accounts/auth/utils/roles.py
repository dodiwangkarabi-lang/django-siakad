def is_dosen(request):
    if (not request.user.is_authenticated): return False
    
    return request.user.groups.filter(name="dosen").exists()

def is_mahasiswa(request):
    if (not request.user.is_authenticated): return False
    
    return request.user.groups.filter(name="mahasiswa").exists()

def tu(request):
    if (not request.user.is_authenticated): return False
    
    return request.user.groups.filter(name="tu").exists()

def get_role(request):
    if is_dosen(request): return "dosen"
    if is_mahasiswa(request): return "mahasiswa"
    if tu(request): return "tu"