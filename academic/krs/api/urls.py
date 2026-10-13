app_name = "academic_krs_api"

from django.urls import path

from . import views
from .views import mhs_views
from .views import dosen_views
from .views import tu_views

urlpatterns = [
    # dosen view
    # path("setujui-krs/<int:krs_id>/", dosen_views.SetujuiKRSAPIView.as_view(), name="setujui_krs"),
    path("detail-krs-mahasiswa/<int:krs_id>/", dosen_views.DetailKRSMahasiswaAPIView.as_view(), name="detail_krs_mahasiswa"),
    # path("tolak-krs/", dosen_views.TolakKRSAPIView.as_view(), name="tolak_krs"),
    # path("minta-perbaiki/", dosen_views.MintaPerbaikiAPIView.as_view(), name="minta_perbaiki"),
    path("periode-krs-aktif/", views.PeriodeKRSAktifAPIView.as_view(), name="periode_krs_aktif"),
    
    # views
    path("semua-kelas-aktif/<int:periode_id>/", views.SemuaKelasAktifAPIView.as_view(), name="semua_kelas_aktif"),
    path("krs-kelas-pasarwajo/", views.KRSKelasPasarwajoAPIView.as_view(), name="krs_kelas_pasarwajo"),
    
    # mahasiswa view
    path("krs-saya/", mhs_views.KRSSayaAPIView.as_view(), name="krs_mahasiswa"),
    path("krs/<int:krs_id>/mahasiswa/", mhs_views.KRSMahasiswaAPIView.as_view(), name="krs_mahasiswa"),
    path("penarawan-krs/periode/<int:periode_id>/", mhs_views.PenarawanKRSAPIView.as_view(), name="penarawan_krs"),
    path("ajukan-krs/", mhs_views.AjukanKRSAPIView.as_view(), name="ajukan_krs"),
    path("cetak-krs/<int:krs_id>/", mhs_views.CetakKRSAPIView.as_view(), name="cetak_krs"),
    path("hapus-item-dalam-krs/", mhs_views.HapusItemKRSAPIView.as_view(), name="hapus_item_dalam_krs"),
    path("buat-krs/", mhs_views.BuatKRSAPIView.as_view(), name="buat_krs"),
    path("lihat-krs-aktif/", views.LihatKRSAktif.as_view(), name="lihat_krs_aktif"),
    path("tambah-kelas/", mhs_views.TambahKelasAPIView.as_view(), name="tambah_kelas"),
    path("tambah-banyak-kelas/", mhs_views.TambahBanyakKelasAPIView.as_view(), name="tambah_banyak_kelas"),
    path("lihat-kelas-dipilih/<int:krs_id>/", mhs_views.KelasDipilihAPIView.as_view(), name="lihat_kelas_dipilih"),
    
    # dosen
    path("validasi-krs", dosen_views.ValidasiKRSAPIView.as_view(), name="krs_validasi_krs"),
    path("krs-diajukan", dosen_views.KRSDiajukanAPIView.as_view(), name="krs_diajukan"),
    path("ajukan-banyak-krs/", dosen_views.AjukanBanyak.as_view(), name="krs_ajukan_banyak"),
    path("daftar-mata-kuliah/", dosen_views.DaftarMataKuliahAPIView.as_view(), name="daftar_mata_kuliah"),
    path("peserta-kelas/<int:kelas_id>/", dosen_views.DaftarPesertaKelas.as_view(), name="daftar_peserta_kelas"),
    path("tambah-peserta-kelas/<int:kelas_id>/", dosen_views.TambahPesertaKelas.as_view(), name="tambah_peserta_kelas"),
    # path("tambah-peserta-kelas/<int:kelas_id>/", dosen_views.TambahPesertaKelas.as_view(), name="tambah_peserta_kelas"),
    path("daftar-mahasiswa-by-angkatan/<int:angkatan>/", dosen_views.DaftarMahasiswaByAngkatan.as_view(), name="daftar_mahasiswa_by_angkatan"),
    path("mahasiswa-aktif/", dosen_views.MahasiswaAktif.as_view(), name="mahasiswa_aktif"),
    path("kelas-aktif/", dosen_views.KelasAktif.as_view(), name="kelas_aktif"),
    
    # tu
    path("mahasiswa-krs-selesai/", tu_views.MahasiswaKRSSelesaiAPIView.as_view(), name="mahasiswa_krs_selesai"),
    path("detail-krs/<int:krs_id>/", tu_views.DetailKRS.as_view(), name="detail_krs"),
    path("mata-kuliah-kelas/", tu_views.MataKuliahKelasAPIView.as_view(), name="mata_kuliah_kelas"),
    path("penawaran-mata-kuliah-kelas/", tu_views.PenawaranMataKuliahKelasAPIView.as_view(), name="penawaran_mata_kuliah_kelas"),
    path("krs-peserta-kelas/<int:kelas_id>/", tu_views.KRSPesertaAPIView.as_view(), name="krs_peserta"),
    path("gabung-banyak-kelas/", tu_views.GabungBanyakKelasAPIView.as_view(), name="gabung_banyak_kelas"),
    path("tambah-kelas/<int:mata_kuliah_id>/", tu_views.TambahKelasAPIView.as_view(), name="tambah_kelas"),
    path("hapus-kelas/<int:kelas_id>/", tu_views.HapusKelasAPIView.as_view(), name="hapus_kelas"),
    path("ganti-nama-kelas/<int:kelas_id>/", tu_views.GantiNamaKelasAPIView.as_view(), name="ganti_nama_kelas"),
    path("download-daftar-hadir/<int:kelas_id>/", tu_views.DownloadDaftarHadir.as_view(), name="download_daftar_hadir"),
    
]