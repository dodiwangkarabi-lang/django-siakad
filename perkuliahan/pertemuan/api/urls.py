from django.urls import path

app_name = "perkuliahan_pertemuan_api"

from . import views

urlpatterns = [
    path("kelas-semua/", views.KelasAPIView.as_view(), name="kelas_semua"),
    path("<int:kumpul_tugas_id>/nilai-tugas/", views.PertemuanNilaiTugasAPIView.as_view(), name="pertemuan_nilai_tugas"),
    path("<int:kumpul_tugas_id>/hapus-tugas-dikumpul/", views.PertemuanHapusTugasDikumpulAPIView.as_view(), name="pertemuan_hapus_tugas_dikumpul"),
    path("<pertemuan_id>/is-mahasiswa-sudah-isi-kehadiran/", views.IsMahasiswaSudahIsiKehadiran.as_view(), name="is_mahasiswa_sudah_isi_kehadiran"),
    path("<kelas_id>/kehadiran-by-kelas/", views.KehadiranByKelasAPIView.as_view(), name="kehadiran_by_kelas"),
    path("<kelas_id>/hitung-point/", views.HitungPointAPIView.as_view(), name="hitung_point"),
    path("<kelas_id>/lihat-nilai-tugas/", views.LihatNilaiTugasAPIView.as_view(), name="lihat_nilai_tugas"),
    path("<kelas_id>/pertemuan-aktif/", views.PertemuanAktifAPIView.as_view(), name="pertemuan_aktif"),
    path("pertemuan-sedang-berlangsung/", views.PertemuanSedangBerlangsungAPIView.as_view(), name="pertemuan_sedang_berlangsung"),
    path("tugas-aktif/", views.TugasAktifAPIView.as_view(), name="tugas_aktif"),
    path("tugas-by-mahasiswa/", views.TugasMahasiswaAPIView.as_view(), name="tugas_mahasiswa"),
    path("<kelas_id>/pertemuan-create/", views.PertemuanCreateAPIView.as_view(), name="pertemuan_create"),
    path("<kelas_id>/pertemuan-all/", views.PertemuanAPIView.as_view(), name="pertemuan_all"),
    path("<int:tugas_id>/edit-tugas/", views.TugasDetailAPIView.as_view(), name="tugas_edit"),
    path("<int:tugas_id>/<int:pertemuan_id>/kirim-tugas/", views.PertemuanKirimTugasAPIView.as_view(), name="pertemuan_kirim_tugas"),
    path("<int:tugas_id>/hapus-tugas/", views.PertemuanHapusTugasAPIView.as_view(), name="pertemuan_hapus_tugas"),
    path("<int:mahasiswa_id>/<int:tugas_id>/hapus-tugas-mahasiswa/", views.PertemuanHapusTugasMahasiswaAPIView.as_view(), name="pertemuan_hapus_tugas_mahasiswa"),
    path("<pertemuan_id>/delete/", views.PertemuanDeleteAPIView.as_view(), name="pertemuan_delete"),
    path("<pertemuan_id>/daftar-hadir-perlu-konfirmasi/", views.DaftarHadirPerluKonfirmasiAPIView.as_view(), name="daftar_hadir_perlu_konfirmasi"),
    path("<pertemuan_id>/", views.PertemuanDetailAPIView.as_view(), name="pertemuan_detail"),
    path("<pertemuan_id>/upload-tugas/", views.PertemuanUploadTugasAPIView.as_view(), name="pertemuan_upload_tugas"),
    path("<pertemuan_id>/semua-tugas/", views.PertemuanSemuaTugasAPIView.as_view(), name="pertemuan_semua_tugas"),
    path("<kelas_id>/kelas-detail/", views.KelasDetailAPIView.as_view(), name="kelas_detail"),
    path("<kelas_id>/semua-tugas-kelas/", views.PertemuanSemuaTugasKelasAPIView.as_view(), name="pertemuan_semua_tugas_kelas"),
    path("<pertemuan_id>/isi-kehadiran/", views.PertemuanIsiKehadiranAPIView.as_view(), name="pertemuan_isi_kehadiran"),
    path("<pertemuan_id>/daftar-kehadiran/", views.PertemuanDaftarKehadiranAPIView.as_view(), name="pertemuan_daftar_kehadiran"),
    path("<pertemuan_id>/daftar-kehadiran-mahasiswa/", views.PertemuanDaftarKehadiranMahasiswaAPIView.as_view(), name="pertemuan_daftar_kehadiran_mahasiswa"),
    path("<kehadiran_id>/verifikasi-kehadiran/", views.PertemuanVerifikasiKehadiranAPIView.as_view(), name="pertemuan_verifikasi_kehadiran"),
    path("<pertemuan_id>/verifikasi-banyak-kehadiran/", views.PertemuanVerifikasiBanyakKehadiranAPIView.as_view(), name="pertemuan_verifikasi_banyak_kehadiran"),
    path("tugas/<tugas_id>/", views.PertemuanTugasDetailAPIView.as_view(), name="pertemuan_tugas_detail"),
    path("tugas/<tugas_id>/kumpulan-tugas-mahasiswa/", views.KumpulanTugasMahasiswaAPIView.as_view(), name="kumpulan_tugas_mahasiswa"),
]
