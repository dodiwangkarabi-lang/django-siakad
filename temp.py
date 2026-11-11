
(globalenv) D:\PROGRAMMING\Projects\siakad\siakad_django>python manage.py show_urls
/       core.views.index        core:index
/academic/api/  rest_framework.routers.APIRootView      api-root
/academic/api/<drf_format_suffix:format>        rest_framework.routers.APIRootView      api-root
/academic/api/detail/   academic.views.DetailKRSAPIView index
/academic/api/detailkrs/        academic.views.DetailKRSView    detailkrs-list
/academic/api/detailkrs/<pk>/   academic.views.DetailKRSView    detailkrs-detail
/academic/api/detailkrs/<pk>\.<format>/ academic.views.DetailKRSView    detailkrs-detail
/academic/api/detailkrs\.<format>/      academic.views.DetailKRSView    detailkrs-list
/academic/api/fakultas/ academic.views.FakultasView     fakultas-list
/academic/api/fakultas/<pk>/    academic.views.FakultasView     fakultas-detail
/academic/api/fakultas/<pk>\.<format>/  academic.views.FakultasView     fakultas-detail
/academic/api/fakultas\.<format>/       academic.views.FakultasView     fakultas-list
/academic/api/kelas/    academic.views.KelasView        kelas-list
/academic/api/kelas/<pk>/       academic.views.KelasView        kelas-detail
/academic/api/kelas/<pk>\.<format>/     academic.views.KelasView        kelas-detail
/academic/api/kelas\.<format>/  academic.views.KelasView        kelas-list
/academic/api/kelola-kelas/jadwal/dosen-pengampu/       academic.kelola_kelas.jadwal.views.DosenPengampuAPIView academic_kelola_kelas_api:jadwal_api:dosen_pengampu
/academic/api/kelola-kelas/jadwal/download-jadwal/      academic.kelola_kelas.jadwal.views.DownloadJadwalAPIView        academic_kelola_kelas_api:jadwal_api:download_jadwal
/academic/api/kelola-kelas/jadwal/hapus-dosen-pengampu/<int:kelas_id>/  academic.kelola_kelas.jadwal.views.HapusDosenPengampuAPIView    academic_kelola_kelas_api:jadwal_api:hapus_dosen_pengampu
/academic/api/kelola-kelas/jadwal/jadwal/       academic.kelola_kelas.jadwal.views.JadwalAPIView        academic_kelola_kelas_api:jadwal_api:jadwal
/academic/api/kelola-kelas/jadwal/kelas-list/   academic.kelola_kelas.jadwal.views.KelasListAPIView     academic_kelola_kelas_api:jadwal_api:kelas_list
/academic/api/kelola-kelas/jadwal/set-dosen-pengampu/<int:kelas_id>/    academic.kelola_kelas.jadwal.views.SetDosenPengampuAPIView      academic_kelola_kelas_api:jadwal_api:set_dosen_pengampu
/academic/api/krs/      academic.views.KRSView  krs-list
/academic/api/krs/<pk>/ academic.views.KRSView  krs-detail
/academic/api/krs/<pk>\.<format>/       academic.views.KRSView  krs-detail
/academic/api/krs/ajukan-banyak-krs/    academic.krs.api.views.dosen_views.AjukanBanyak academic_krs_api:krs_ajukan_banyak
/academic/api/krs/ajukan-krs/   academic.krs.api.views.mhs_views.AjukanKRSAPIView       academic_krs_api:ajukan_krs
/academic/api/krs/buat-krs/     academic.krs.api.views.mhs_views.BuatKRSAPIView academic_krs_api:buat_krs
/academic/api/krs/cetak-krs/<int:krs_id>/       academic.krs.api.views.mhs_views.CetakKRSAPIView        academic_krs_api:cetak_krs
/academic/api/krs/daftar-mahasiswa-by-angkatan/<int:angkatan>/  academic.krs.api.views.dosen_views.DaftarMahasiswaByAngkatan    academic_krs_api:daftar_mahasiswa_by_angkatan
/academic/api/krs/daftar-mata-kuliah/   academic.krs.api.views.dosen_views.DaftarMataKuliahAPIView      academic_krs_api:daftar_mata_kuliah
/academic/api/krs/detail-krs-mahasiswa/<int:krs_id>/    academic.krs.api.views.dosen_views.DetailKRSMahasiswaAPIView    academic_krs_api:detail_krs_mahasiswa
/academic/api/krs/detail-krs/<int:krs_id>/      academic.krs.api.views.tu_views.DetailKRS       academic_krs_api:detail_krs
/academic/api/krs/download-daftar-hadir/<int:kelas_id>/ academic.krs.api.views.tu_views.DownloadDaftarHadir     academic_krs_api:download_daftar_hadir
/academic/api/krs/gabung-banyak-kelas/  academic.krs.api.views.tu_views.GabungBanyakKelasAPIView        academic_krs_api:gabung_banyak_kelas
/academic/api/krs/ganti-nama-kelas/<int:kelas_id>/      academic.krs.api.views.tu_views.GantiNamaKelasAPIView   academic_krs_api:ganti_nama_kelas
/academic/api/krs/hapus-item-dalam-krs/ academic.krs.api.views.mhs_views.HapusItemKRSAPIView    academic_krs_api:hapus_item_dalam_krs
/academic/api/krs/hapus-kelas/<int:kelas_id>/   academic.krs.api.views.tu_views.HapusKelasAPIView       academic_krs_api:hapus_kelas
/academic/api/krs/kelas-aktif/  academic.krs.api.views.dosen_views.KelasAktif   academic_krs_api:kelas_aktif
/academic/api/krs/krs-diajukan  academic.krs.api.views.dosen_views.KRSDiajukanAPIView   academic_krs_api:krs_diajukan
/academic/api/krs/krs-kelas-pasarwajo/  academic.krs.api.views.views.KRSKelasPasarwajoAPIView   academic_krs_api:krs_kelas_pasarwajo
/academic/api/krs/krs-peserta-kelas/<int:kelas_id>/     academic.krs.api.views.tu_views.KRSPesertaAPIView       academic_krs_api:krs_peserta
/academic/api/krs/krs-saya/     academic.krs.api.views.mhs_views.KRSSayaAPIView academic_krs_api:krs_mahasiswa
/academic/api/krs/krs/<int:krs_id>/mahasiswa/   academic.krs.api.views.mhs_views.KRSMahasiswaAPIView    academic_krs_api:krs_mahasiswa
/academic/api/krs/lihat-kelas-dipilih/<int:krs_id>/     academic.krs.api.views.mhs_views.KelasDipilihAPIView    academic_krs_api:lihat_kelas_dipilih
/academic/api/krs/lihat-krs-aktif/      academic.krs.api.views.views.LihatKRSAktif      academic_krs_api:lihat_krs_aktif
/academic/api/krs/mahasiswa-aktif/      academic.krs.api.views.dosen_views.MahasiswaAktif       academic_krs_api:mahasiswa_aktif
/academic/api/krs/mahasiswa-krs-selesai/        academic.krs.api.views.tu_views.MahasiswaKRSSelesaiAPIView      academic_krs_api:mahasiswa_krs_selesai
/academic/api/krs/mata-kuliah-kelas/    academic.krs.api.views.tu_views.MataKuliahKelasAPIView  academic_krs_api:mata_kuliah_kelas
/academic/api/krs/penarawan-krs/periode/<int:periode_id>/       academic.krs.api.views.mhs_views.PenarawanKRSAPIView    academic_krs_api:penarawan_krs
/academic/api/krs/penawaran-mata-kuliah-kelas/  academic.krs.api.views.tu_views.PenawaranMataKuliahKelasAPIView academic_krs_api:penawaran_mata_kuliah_kelas
/academic/api/krs/periode-krs-aktif/    academic.krs.api.views.views.PeriodeKRSAktifAPIView     academic_krs_api:periode_krs_aktif
/academic/api/krs/peserta-kelas/<int:kelas_id>/ academic.krs.api.views.dosen_views.DaftarPesertaKelas   academic_krs_api:daftar_peserta_kelas
/academic/api/krs/semua-kelas-aktif/<int:periode_id>/   academic.krs.api.views.views.SemuaKelasAktifAPIView     academic_krs_api:semua_kelas_aktif
/academic/api/krs/tambah-banyak-kelas/  academic.krs.api.views.mhs_views.TambahBanyakKelasAPIView       academic_krs_api:tambah_banyak_kelas
/academic/api/krs/tambah-kelas/ academic.krs.api.views.mhs_views.TambahKelasAPIView     academic_krs_api:tambah_kelas
/academic/api/krs/tambah-kelas/<int:mata_kuliah_id>/    academic.krs.api.views.tu_views.TambahKelasAPIView      academic_krs_api:tambah_kelas
/academic/api/krs/tambah-peserta-kelas/<int:kelas_id>/  academic.krs.api.views.dosen_views.TambahPesertaKelas   academic_krs_api:tambah_peserta_kelas
/academic/api/krs/validasi-krs  academic.krs.api.views.dosen_views.ValidasiKRSAPIView   academic_krs_api:krs_validasi_krs
/academic/api/krs\.<format>/    academic.views.KRSView  krs-list
/academic/api/matkul/   academic.views.MataKuliahView   matakuliah-list
/academic/api/matkul/<pk>/      academic.views.MataKuliahView   matakuliah-detail
/academic/api/matkul/<pk>\.<format>/    academic.views.MataKuliahView   matakuliah-detail
/academic/api/matkul\.<format>/ academic.views.MataKuliahView   matakuliah-list
/academic/api/prodi/    academic.views.ProdiView        prodi-list
/academic/api/prodi/<pk>/       academic.views.ProdiView        prodi-detail
/academic/api/prodi/<pk>\.<format>/     academic.views.ProdiView        prodi-detail
/academic/api/prodi\.<format>/  academic.views.ProdiView        prodi-list
/accounts/api/  rest_framework.routers.APIRootView      api-root
/accounts/api/<drf_format_suffix:format>        rest_framework.routers.APIRootView      api-root
/accounts/api/dosen/    accounts.views.DosenViewSet     dosen-list
/accounts/api/dosen/<pk>/       accounts.views.DosenViewSet     dosen-detail
/accounts/api/dosen/<pk>\.<format>/     accounts.views.DosenViewSet     dosen-detail
/accounts/api/dosen\.<format>/  accounts.views.DosenViewSet     dosen-list
/accounts/api/mahasiswa/        accounts.views.MahasiswaViewSet mahasiswa-list
/accounts/api/mahasiswa/<pk>/   accounts.views.MahasiswaViewSet mahasiswa-detail
/accounts/api/mahasiswa/<pk>\.<format>/ accounts.views.MahasiswaViewSet mahasiswa-detail
/accounts/api/mahasiswa/biodata-mahasiswa/      accounts.mahasiswa.api.views.BiodataMahasiswaAPIView    accounts_mahasiswa_api:biodata_mahasiswa
/accounts/api/mahasiswa/semua/nim/      accounts.mahasiswa.api.views.SemuaNimAPIView    accounts_mahasiswa_api:semua_nim
/accounts/api/mahasiswa\.<format>/      accounts.views.MahasiswaViewSet mahasiswa-list
/accounts/api/user/     accounts.views.UserViewSet      user-list
/accounts/api/user/<pk>/        accounts.views.UserViewSet      user-detail
/accounts/api/user/<pk>\.<format>/      accounts.views.UserViewSet      user-detail
/accounts/api/user\.<format>/   accounts.views.UserViewSet      user-list
/admin/ django.contrib.admin.sites.index        admin:index
/admin/<app_label>/     django.contrib.admin.sites.app_index    admin:app_list
/admin/<url>    django.contrib.admin.sites.catch_all_view
/admin/academic/detailkrs/      django.contrib.admin.options.changelist_view    admin:academic_detailkrs_changelist
/admin/academic/detailkrs/<path:object_id>/     django.views.generic.base.RedirectView
/admin/academic/detailkrs/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:academic_detailkrs_change
/admin/academic/detailkrs/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:academic_detailkrs_delete
/admin/academic/detailkrs/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:academic_detailkrs_history
/admin/academic/detailkrs/add/  django.contrib.admin.options.add_view   admin:academic_detailkrs_add
/admin/academic/fakultas/       django.contrib.admin.options.changelist_view    admin:academic_fakultas_changelist
/admin/academic/fakultas/<path:object_id>/      django.views.generic.base.RedirectView
/admin/academic/fakultas/<path:object_id>/change/       django.contrib.admin.options.change_view        admin:academic_fakultas_change
/admin/academic/fakultas/<path:object_id>/delete/       django.contrib.admin.options.delete_view        admin:academic_fakultas_delete
/admin/academic/fakultas/<path:object_id>/history/      django.contrib.admin.options.history_view       admin:academic_fakultas_history
/admin/academic/fakultas/add/   django.contrib.admin.options.add_view   admin:academic_fakultas_add
/admin/academic/kelas/  django.contrib.admin.options.changelist_view    admin:academic_kelas_changelist
/admin/academic/kelas/<path:object_id>/ django.views.generic.base.RedirectView
/admin/academic/kelas/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:academic_kelas_change
/admin/academic/kelas/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:academic_kelas_delete
/admin/academic/kelas/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:academic_kelas_history
/admin/academic/kelas/add/      django.contrib.admin.options.add_view   admin:academic_kelas_add
/admin/academic/komponennilai/  django.contrib.admin.options.changelist_view    admin:academic_komponennilai_changelist
/admin/academic/komponennilai/<path:object_id>/ django.views.generic.base.RedirectView
/admin/academic/komponennilai/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:academic_komponennilai_change
/admin/academic/komponennilai/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:academic_komponennilai_delete
/admin/academic/komponennilai/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:academic_komponennilai_history
/admin/academic/komponennilai/add/      django.contrib.admin.options.add_view   admin:academic_komponennilai_add
/admin/academic/krs/    django.contrib.admin.options.changelist_view    admin:academic_krs_changelist
/admin/academic/krs/<path:object_id>/   django.views.generic.base.RedirectView
/admin/academic/krs/<path:object_id>/change/    django.contrib.admin.options.change_view        admin:academic_krs_change
/admin/academic/krs/<path:object_id>/delete/    django.contrib.admin.options.delete_view        admin:academic_krs_delete
/admin/academic/krs/<path:object_id>/history/   django.contrib.admin.options.history_view       admin:academic_krs_history
/admin/academic/krs/add/        django.contrib.admin.options.add_view   admin:academic_krs_add
/admin/academic/kurikulum/      django.contrib.admin.options.changelist_view    admin:academic_kurikulum_changelist
/admin/academic/kurikulum/<path:object_id>/     django.views.generic.base.RedirectView
/admin/academic/kurikulum/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:academic_kurikulum_change
/admin/academic/kurikulum/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:academic_kurikulum_delete
/admin/academic/kurikulum/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:academic_kurikulum_history
/admin/academic/kurikulum/add/  django.contrib.admin.options.add_view   admin:academic_kurikulum_add
/admin/academic/kurikulummatakuliah/    django.contrib.admin.options.changelist_view    admin:academic_kurikulummatakuliah_changelist
/admin/academic/kurikulummatakuliah/<path:object_id>/   django.views.generic.base.RedirectView
/admin/academic/kurikulummatakuliah/<path:object_id>/change/    django.contrib.admin.options.change_view        admin:academic_kurikulummatakuliah_change
/admin/academic/kurikulummatakuliah/<path:object_id>/delete/    django.contrib.admin.options.delete_view        admin:academic_kurikulummatakuliah_delete
/admin/academic/kurikulummatakuliah/<path:object_id>/history/   django.contrib.admin.options.history_view       admin:academic_kurikulummatakuliah_history
/admin/academic/kurikulummatakuliah/add/        django.contrib.admin.options.add_view   admin:academic_kurikulummatakuliah_add
/admin/academic/matakuliah/     django.contrib.admin.options.changelist_view    admin:academic_matakuliah_changelist
/admin/academic/matakuliah/<path:object_id>/    django.views.generic.base.RedirectView
/admin/academic/matakuliah/<path:object_id>/change/     django.contrib.admin.options.change_view        admin:academic_matakuliah_change
/admin/academic/matakuliah/<path:object_id>/delete/     django.contrib.admin.options.delete_view        admin:academic_matakuliah_delete
/admin/academic/matakuliah/<path:object_id>/history/    django.contrib.admin.options.history_view       admin:academic_matakuliah_history
/admin/academic/matakuliah/add/ django.contrib.admin.options.add_view   admin:academic_matakuliah_add
/admin/academic/nilai/  django.contrib.admin.options.changelist_view    admin:academic_nilai_changelist
/admin/academic/nilai/<path:object_id>/ django.views.generic.base.RedirectView
/admin/academic/nilai/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:academic_nilai_change
/admin/academic/nilai/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:academic_nilai_delete
/admin/academic/nilai/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:academic_nilai_history
/admin/academic/nilai/add/      django.contrib.admin.options.add_view   admin:academic_nilai_add
/admin/academic/nilaikomponen/  django.contrib.admin.options.changelist_view    admin:academic_nilaikomponen_changelist
/admin/academic/nilaikomponen/<path:object_id>/ django.views.generic.base.RedirectView
/admin/academic/nilaikomponen/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:academic_nilaikomponen_change
/admin/academic/nilaikomponen/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:academic_nilaikomponen_delete
/admin/academic/nilaikomponen/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:academic_nilaikomponen_history
/admin/academic/nilaikomponen/add/      django.contrib.admin.options.add_view   admin:academic_nilaikomponen_add
/admin/academic/penawarankrs/   django.contrib.admin.options.changelist_view    admin:academic_penawarankrs_changelist
/admin/academic/penawarankrs/<path:object_id>/  django.views.generic.base.RedirectView
/admin/academic/penawarankrs/<path:object_id>/change/   django.contrib.admin.options.change_view        admin:academic_penawarankrs_change
/admin/academic/penawarankrs/<path:object_id>/delete/   django.contrib.admin.options.delete_view        admin:academic_penawarankrs_delete
/admin/academic/penawarankrs/<path:object_id>/history/  django.contrib.admin.options.history_view       admin:academic_penawarankrs_history
/admin/academic/penawarankrs/add/       django.contrib.admin.options.add_view   admin:academic_penawarankrs_add
/admin/academic/periodekrs/     django.contrib.admin.options.changelist_view    admin:academic_periodekrs_changelist
/admin/academic/periodekrs/<path:object_id>/    django.views.generic.base.RedirectView
/admin/academic/periodekrs/<path:object_id>/change/     django.contrib.admin.options.change_view        admin:academic_periodekrs_change
/admin/academic/periodekrs/<path:object_id>/delete/     django.contrib.admin.options.delete_view        admin:academic_periodekrs_delete
/admin/academic/periodekrs/<path:object_id>/history/    django.contrib.admin.options.history_view       admin:academic_periodekrs_history
/admin/academic/periodekrs/add/ django.contrib.admin.options.add_view   admin:academic_periodekrs_add
/admin/academic/prodi/  django.contrib.admin.options.changelist_view    admin:academic_prodi_changelist
/admin/academic/prodi/<path:object_id>/ django.views.generic.base.RedirectView
/admin/academic/prodi/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:academic_prodi_change
/admin/academic/prodi/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:academic_prodi_delete
/admin/academic/prodi/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:academic_prodi_history
/admin/academic/prodi/add/      django.contrib.admin.options.add_view   admin:academic_prodi_add
/admin/accounts/dosen/  django.contrib.admin.options.changelist_view    admin:accounts_dosen_changelist
/admin/accounts/dosen/<path:object_id>/ django.views.generic.base.RedirectView
/admin/accounts/dosen/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:accounts_dosen_change
/admin/accounts/dosen/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:accounts_dosen_delete
/admin/accounts/dosen/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:accounts_dosen_history
/admin/accounts/dosen/add/      django.contrib.admin.options.add_view   admin:accounts_dosen_add
/admin/accounts/mahasiswa/      django.contrib.admin.options.changelist_view    admin:accounts_mahasiswa_changelist
/admin/accounts/mahasiswa/<path:object_id>/     django.views.generic.base.RedirectView
/admin/accounts/mahasiswa/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:accounts_mahasiswa_change
/admin/accounts/mahasiswa/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:accounts_mahasiswa_delete
/admin/accounts/mahasiswa/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:accounts_mahasiswa_history
/admin/accounts/mahasiswa/add/  django.contrib.admin.options.add_view   admin:accounts_mahasiswa_add
/admin/accounts/tandatangan/    django.contrib.admin.options.changelist_view    admin:accounts_tandatangan_changelist
/admin/accounts/tandatangan/<path:object_id>/   django.views.generic.base.RedirectView
/admin/accounts/tandatangan/<path:object_id>/change/    django.contrib.admin.options.change_view        admin:accounts_tandatangan_change
/admin/accounts/tandatangan/<path:object_id>/delete/    django.contrib.admin.options.delete_view        admin:accounts_tandatangan_delete
/admin/accounts/tandatangan/<path:object_id>/history/   django.contrib.admin.options.history_view       admin:accounts_tandatangan_history
/admin/accounts/tandatangan/add/        django.contrib.admin.options.add_view   admin:accounts_tandatangan_add
/admin/auth/group/      django.contrib.admin.options.changelist_view    admin:auth_group_changelist
/admin/auth/group/<path:object_id>/     django.views.generic.base.RedirectView
/admin/auth/group/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:auth_group_change
/admin/auth/group/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:auth_group_delete
/admin/auth/group/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:auth_group_history
/admin/auth/group/add/  django.contrib.admin.options.add_view   admin:auth_group_add
/admin/auth/user/       django.contrib.admin.options.changelist_view    admin:auth_user_changelist
/admin/auth/user/<id>/password/ django.contrib.auth.admin.user_change_password  admin:auth_user_password_change
/admin/auth/user/<path:object_id>/      django.views.generic.base.RedirectView
/admin/auth/user/<path:object_id>/change/       django.contrib.admin.options.change_view        admin:auth_user_change
/admin/auth/user/<path:object_id>/delete/       django.contrib.admin.options.delete_view        admin:auth_user_delete
/admin/auth/user/<path:object_id>/history/      django.contrib.admin.options.history_view       admin:auth_user_history
/admin/auth/user/add/   django.contrib.auth.admin.add_view      admin:auth_user_add
/admin/autocomplete/    django.contrib.admin.sites.autocomplete_view    admin:autocomplete
/admin/jsi18n/  django.contrib.admin.sites.i18n_javascript      admin:jsi18n
/admin/login/   django.contrib.admin.sites.login        admin:login
/admin/logout/  django.contrib.admin.sites.logout       admin:logout
/admin/password_change/ django.contrib.admin.sites.password_change      admin:password_change
/admin/password_change/done/    django.contrib.admin.sites.password_change_done admin:password_change_done
/admin/penugasan/pengumpulantugas/      django.contrib.admin.options.changelist_view    admin:penugasan_pengumpulantugas_changelist
/admin/penugasan/pengumpulantugas/<path:object_id>/     django.views.generic.base.RedirectView
/admin/penugasan/pengumpulantugas/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:penugasan_pengumpulantugas_change
/admin/penugasan/pengumpulantugas/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:penugasan_pengumpulantugas_delete
/admin/penugasan/pengumpulantugas/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:penugasan_pengumpulantugas_history
/admin/penugasan/pengumpulantugas/add/  django.contrib.admin.options.add_view   admin:penugasan_pengumpulantugas_add
/admin/penugasan/penugasan/     django.contrib.admin.options.changelist_view    admin:penugasan_penugasan_changelist
/admin/penugasan/penugasan/<path:object_id>/    django.views.generic.base.RedirectView
/admin/penugasan/penugasan/<path:object_id>/change/     django.contrib.admin.options.change_view        admin:penugasan_penugasan_change
/admin/penugasan/penugasan/<path:object_id>/delete/     django.contrib.admin.options.delete_view        admin:penugasan_penugasan_delete
/admin/penugasan/penugasan/<path:object_id>/history/    django.contrib.admin.options.history_view       admin:penugasan_penugasan_history
/admin/penugasan/penugasan/add/ django.contrib.admin.options.add_view   admin:penugasan_penugasan_add
/admin/perkuliahan/kehadiran/   django.contrib.admin.options.changelist_view    admin:perkuliahan_kehadiran_changelist
/admin/perkuliahan/kehadiran/<path:object_id>/  django.views.generic.base.RedirectView
/admin/perkuliahan/kehadiran/<path:object_id>/change/   django.contrib.admin.options.change_view        admin:perkuliahan_kehadiran_change
/admin/perkuliahan/kehadiran/<path:object_id>/delete/   django.contrib.admin.options.delete_view        admin:perkuliahan_kehadiran_delete
/admin/perkuliahan/kehadiran/<path:object_id>/history/  django.contrib.admin.options.history_view       admin:perkuliahan_kehadiran_history
/admin/perkuliahan/kehadiran/add/       django.contrib.admin.options.add_view   admin:perkuliahan_kehadiran_add
/admin/perkuliahan/kumpultugas/ django.contrib.admin.options.changelist_view    admin:perkuliahan_kumpultugas_changelist
/admin/perkuliahan/kumpultugas/<path:object_id>/        django.views.generic.base.RedirectView
/admin/perkuliahan/kumpultugas/<path:object_id>/change/ django.contrib.admin.options.change_view        admin:perkuliahan_kumpultugas_change
/admin/perkuliahan/kumpultugas/<path:object_id>/delete/ django.contrib.admin.options.delete_view        admin:perkuliahan_kumpultugas_delete
/admin/perkuliahan/kumpultugas/<path:object_id>/history/        django.contrib.admin.options.history_view       admin:perkuliahan_kumpultugas_history
/admin/perkuliahan/kumpultugas/add/     django.contrib.admin.options.add_view   admin:perkuliahan_kumpultugas_add
/admin/perkuliahan/nilai/       django.contrib.admin.options.changelist_view    admin:perkuliahan_nilai_changelist
/admin/perkuliahan/nilai/<path:object_id>/      django.views.generic.base.RedirectView
/admin/perkuliahan/nilai/<path:object_id>/change/       django.contrib.admin.options.change_view        admin:perkuliahan_nilai_change
/admin/perkuliahan/nilai/<path:object_id>/delete/       django.contrib.admin.options.delete_view        admin:perkuliahan_nilai_delete
/admin/perkuliahan/nilai/<path:object_id>/history/      django.contrib.admin.options.history_view       admin:perkuliahan_nilai_history
/admin/perkuliahan/nilai/add/   django.contrib.admin.options.add_view   admin:perkuliahan_nilai_add
/admin/perkuliahan/pertemuan/   django.contrib.admin.options.changelist_view    admin:perkuliahan_pertemuan_changelist
/admin/perkuliahan/pertemuan/<path:object_id>/  django.views.generic.base.RedirectView
/admin/perkuliahan/pertemuan/<path:object_id>/change/   django.contrib.admin.options.change_view        admin:perkuliahan_pertemuan_change
/admin/perkuliahan/pertemuan/<path:object_id>/delete/   django.contrib.admin.options.delete_view        admin:perkuliahan_pertemuan_delete
/admin/perkuliahan/pertemuan/<path:object_id>/history/  django.contrib.admin.options.history_view       admin:perkuliahan_pertemuan_history
/admin/perkuliahan/pertemuan/add/       django.contrib.admin.options.add_view   admin:perkuliahan_pertemuan_add
/admin/perkuliahan/tugas/       django.contrib.admin.options.changelist_view    admin:perkuliahan_tugas_changelist
/admin/perkuliahan/tugas/<path:object_id>/      django.views.generic.base.RedirectView
/admin/perkuliahan/tugas/<path:object_id>/change/       django.contrib.admin.options.change_view        admin:perkuliahan_tugas_change
/admin/perkuliahan/tugas/<path:object_id>/delete/       django.contrib.admin.options.delete_view        admin:perkuliahan_tugas_delete
/admin/perkuliahan/tugas/<path:object_id>/history/      django.contrib.admin.options.history_view       admin:perkuliahan_tugas_history
/admin/perkuliahan/tugas/add/   django.contrib.admin.options.add_view   admin:perkuliahan_tugas_add
/admin/r/<path:content_type_id>/<path:object_id>/       django.contrib.contenttypes.views.shortcut      admin:view_on_site
/api/auth/get-role/     accounts.auth.api.views.GetRoleAPIView  auth_api:get-role
/api/auth/login/        accounts.auth.api.views.LoginAPIView    auth_api:login
/api/auth/logout/       accounts.auth.api.views.LogoutAPIView   auth_api:logout
/api/auth/me/   accounts.auth.api.views.MeAPIView       auth_api:me
/api/docs/      drf_spectacular.views.SpectacularSwaggerView    swagger-ui
/api/perkuliahan/pertemuan/<int:kumpul_tugas_id>/nilai-tugas/   perkuliahan.pertemuan.api.views.PertemuanNilaiTugasAPIView      perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_nilai_tugas
/api/perkuliahan/pertemuan/<int:mahasiswa_id>/<int:tugas_id>/hapus-tugas-mahasiswa/     perkuliahan.pertemuan.api.views.PertemuanHapusTugasMahasiswaAPIView     perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_hapus_tugas_mahasiswa
/api/perkuliahan/pertemuan/<int:tugas_id>/hapus-tugas/  perkuliahan.pertemuan.api.views.PertemuanHapusTugasAPIView      perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_hapus_tugas
/api/perkuliahan/pertemuan/<int:tugas_id>/kirim-tugas/  perkuliahan.pertemuan.api.views.PertemuanKirimTugasAPIView      perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_kirim_tugas
/api/perkuliahan/pertemuan/<kehadiran_id>/verifikasi-kehadiran/ perkuliahan.pertemuan.api.views.PertemuanVerifikasiKehadiranAPIView     perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_verifikasi_kehadiran
/api/perkuliahan/pertemuan/<kelas_id>/kehadiran-by-kelas/       perkuliahan.pertemuan.api.views.KehadiranByKelasAPIView perkuliahan_api:perkuliahan_pertemuan_api:kehadiran_by_kelas
/api/perkuliahan/pertemuan/<kelas_id>/pertemuan-aktif/  perkuliahan.pertemuan.api.views.PertemuanAktifAPIView   perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_aktif
/api/perkuliahan/pertemuan/<kelas_id>/pertemuan-all/    perkuliahan.pertemuan.api.views.PertemuanAPIView        perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_all
/api/perkuliahan/pertemuan/<kelas_id>/pertemuan-create/ perkuliahan.pertemuan.api.views.PertemuanCreateAPIView  perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_create
/api/perkuliahan/pertemuan/<kelas_id>/semua-tugas-kelas/        perkuliahan.pertemuan.api.views.PertemuanSemuaTugasKelasAPIView perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_semua_tugas_kelas
/api/perkuliahan/pertemuan/<pertemuan_id>/      perkuliahan.pertemuan.api.views.PertemuanDetailAPIView  perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_detail
/api/perkuliahan/pertemuan/<pertemuan_id>/daftar-hadir-perlu-konfirmasi/        perkuliahan.pertemuan.api.views.DaftarHadirPerluKonfirmasiAPIView       perkuliahan_api:perkuliahan_pertemuan_api:daftar_hadir_perlu_konfirmasi
/api/perkuliahan/pertemuan/<pertemuan_id>/daftar-kehadiran-mahasiswa/   perkuliahan.pertemuan.api.views.PertemuanDaftarKehadiranMahasiswaAPIView        perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_daftar_kehadiran_mahasiswa
/api/perkuliahan/pertemuan/<pertemuan_id>/daftar-kehadiran/     perkuliahan.pertemuan.api.views.PertemuanDaftarKehadiranAPIView perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_daftar_kehadiran
/api/perkuliahan/pertemuan/<pertemuan_id>/delete/       perkuliahan.pertemuan.api.views.PertemuanDeleteAPIView  perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_delete
/api/perkuliahan/pertemuan/<pertemuan_id>/is-mahasiswa-sudah-isi-kehadiran/     perkuliahan.pertemuan.api.views.IsMahasiswaSudahIsiKehadiran    perkuliahan_api:perkuliahan_pertemuan_api:is_mahasiswa_sudah_isi_kehadiran
/api/perkuliahan/pertemuan/<pertemuan_id>/isi-kehadiran/        perkuliahan.pertemuan.api.views.PertemuanIsiKehadiranAPIView    perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_isi_kehadiran
/api/perkuliahan/pertemuan/<pertemuan_id>/semua-tugas/  perkuliahan.pertemuan.api.views.PertemuanSemuaTugasAPIView      perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_semua_tugas
/api/perkuliahan/pertemuan/<pertemuan_id>/upload-tugas/ perkuliahan.pertemuan.api.views.PertemuanUploadTugasAPIView     perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_upload_tugas
/api/perkuliahan/pertemuan/<pertemuan_id>/verifikasi-banyak-kehadiran/  perkuliahan.pertemuan.api.views.PertemuanVerifikasiBanyakKehadiranAPIView       perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_verifikasi_banyak_kehadiran
/api/perkuliahan/pertemuan/kelas-semua/ perkuliahan.pertemuan.api.views.KelasAPIView    perkuliahan_api:perkuliahan_pertemuan_api:kelas_semua
/api/perkuliahan/pertemuan/pertemuan-sedang-berlangsung/        perkuliahan.pertemuan.api.views.PertemuanSedangBerlangsungAPIView       perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_sedang_berlangsung
/api/perkuliahan/pertemuan/tugas-aktif/ perkuliahan.pertemuan.api.views.TugasAktifAPIView       perkuliahan_api:perkuliahan_pertemuan_api:tugas_aktif
/api/perkuliahan/pertemuan/tugas-by-mahasiswa/  perkuliahan.pertemuan.api.views.TugasMahasiswaAPIView   perkuliahan_api:perkuliahan_pertemuan_api:tugas_mahasiswa
/api/perkuliahan/pertemuan/tugas/<tugas_id>/    perkuliahan.pertemuan.api.views.PertemuanTugasDetailAPIView     perkuliahan_api:perkuliahan_pertemuan_api:pertemuan_tugas_detail
/api/perkuliahan/pertemuan/tugas/<tugas_id>/kumpulan-tugas-mahasiswa/   perkuliahan.pertemuan.api.views.KumpulanTugasMahasiswaAPIView   perkuliahan_api:perkuliahan_pertemuan_api:kumpulan_tugas_mahasiswa
/api/redoc/     drf_spectacular.views.SpectacularRedocView      redoc
/api/schema/    drf_spectacular.views.SpectacularAPIView        schema
/api/token/     rest_framework_simplejwt.views.TokenObtainPairView      token_obtain_pair
/api/token/refresh/     rest_framework_simplejwt.views.TokenRefreshView token_refresh
/api/token/verify/      rest_framework_simplejwt.views.TokenVerifyView  token_verify
/gabung-kelas/  core.views.gabung_kelas core:gabung_kelas
/kelas/ core.views.kelas        core:kelas
/kelas/<int:kelas_id>/  academic.web.views.kelas_views.detail_kelas     academic:kelas_web:detail_kelas
/kelas/<int:kelas_id>/tugas/    penugasan.web.views.daftar_tugas_by_kelas       penugasan:daftar_tugas_by_kelas
/kelas/daftar-kelas/    academic.web.views.kelas_views.daftar_kelas     academic:kelas_web:daftar_kelas
/kelas/daftar-materi/   academic.web.views.kelas_views.daftar_materi    academic:kelas_web:daftar_materi
/kelola-jadwal/ core.views.kelola_jadwal        core:kelola_jadwal
/kelola-krs/    core.views.kelola_krs   core:kelola_krs
/krs/   core.views.krs  core:krs
/login/ accounts.web.views.login_view   accounts_web:login
/media/<path>   django.views.static.serve
/penugasan/<int:penugasan_id>/pengumpulan/      penugasan.web.views.detail_penugasan    penugasan:detail_penugasan
/submit-krs/    core.views.submit_krs   core:submit_krs
/tugas/ penugasan.web.views.daftar_tugas        penugasan:daftar_tugas
/tugas/<int:penugasan_id>/      penugasan.web.views.kirim_tugas penugasan:kirim_tugas

(globalenv) D:\PROGRAMMING\Projects\siakad\siakad_django>