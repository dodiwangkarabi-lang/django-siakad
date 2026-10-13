from django.contrib import admin

# models
from .models import (
    Penugasan, PengumpulanTugas
)


# Register your models here.
admin.site.register(Penugasan)
admin.site.register(PengumpulanTugas)
