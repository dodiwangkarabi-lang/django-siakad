from rest_framework import serializers

from penugasan.models import (
    PengumpulanTugas, Penugasan
)

class PengumpulanTugasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PengumpulanTugas
        fields = "__all__"
        read_only_fields = ["penugasan", "mahasiswa", "tanggal_kirim"]