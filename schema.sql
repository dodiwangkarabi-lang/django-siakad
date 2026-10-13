CREATE INDEX "academic_detailkrs_kelas_id_cd1f20c7" ON "academic_detailkrs" ("kelas_id");

CREATE INDEX "academic_detailkrs_krs_id_71feaa47" ON "academic_detailkrs" ("krs_id");

CREATE UNIQUE INDEX "academic_detailkrs_krs_id_kelas_id_042c4865_uniq" ON "academic_detailkrs" ("krs_id", "kelas_id");

CREATE INDEX "academic_kelas_dosen_id_710c39da" ON "academic_kelas" ("dosen_id");

CREATE INDEX "academic_kelas_mata_kuliah_id_22c96436" ON "academic_kelas" ("mata_kuliah_id");

CREATE INDEX "academic_krs_mahasiswa_id_988a7338" ON "academic_krs" ("mahasiswa_id");

CREATE INDEX "academic_kurikulum_program_studi_id_5ea45b49" ON "academic_kurikulum" ("program_studi_id");

CREATE INDEX "academic_kurikulummatakuliah_kurikulum_id_25c3f5c1" ON "academic_kurikulummatakuliah" ("kurikulum_id");

CREATE INDEX "academic_kurikulummatakuliah_mata_kuliah_id_0749c209" ON "academic_kurikulummatakuliah" ("mata_kuliah_id");

CREATE INDEX "academic_nilaikomponen_komponen_nilai_id_01000520" ON "academic_nilaikomponen" ("komponen_nilai_id");

CREATE INDEX "academic_nilaikomponen_nilai_id_id_7d0dab98" ON "academic_nilaikomponen" ("nilai_id_id");

CREATE INDEX "academic_penawarankrs_kelas_id_3bcfc74e" ON "academic_penawarankrs" ("kelas_id");

CREATE INDEX "academic_penawarankrs_periode_krs_id_a4b9c1e4" ON "academic_penawarankrs" ("periode_krs_id");

CREATE INDEX "academic_prodi_fakultas_id_6076f6a4" ON "academic_prodi" ("fakultas_id");

CREATE INDEX "accounts_mahasiswa_prodi_id_e79cf2bf" ON "accounts_mahasiswa" ("prodi_id");

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");

CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");

CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");

CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");

CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");

CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

CREATE INDEX "penugasan_pengumpulantugas_mahasiswa_id_c5289a1f" ON "penugasan_pengumpulantugas" ("mahasiswa_id");

CREATE INDEX "penugasan_pengumpulantugas_penugasan_id_fa9a2a8d" ON "penugasan_pengumpulantugas" ("penugasan_id");

CREATE INDEX "penugasan_penugasan_kelas_id_f2c22c91" ON "penugasan_penugasan" ("kelas_id");

CREATE TABLE
    "academic_detailkrs" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "kelas_id" bigint NULL REFERENCES "academic_kelas" ("id") DEFERRABLE INITIALLY DEFERRED,
        "krs_id" bigint NULL REFERENCES "academic_krs" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "academic_fakultas" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "kode" varchar(10) NULL UNIQUE,
        "nama" varchar(100) NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL
    );

CREATE TABLE
    "academic_kelas" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "kode" varchar(10) NULL UNIQUE,
        "nama" varchar(100) NULL,
        "ruangan" varchar(100) NULL,
        "waktu" varchar(100) NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "dosen_id" bigint NULL REFERENCES "accounts_dosen" ("id") DEFERRABLE INITIALLY DEFERRED,
        "mata_kuliah_id" bigint NULL REFERENCES "academic_matakuliah" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "academic_komponennilai" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "nama" varchar(100) NULL,
        "bobot" real NULL,
        CONSTRAINT "bobot_antara_0_dan_100" CHECK (
            (
                "bobot" >= 0.0
                AND "bobot" <= 100.0
            )
        )
    );

CREATE TABLE
    "academic_krs" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "tahun_ajaran" varchar(10) NULL,
        "semester" varchar(10) NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "mahasiswa_id" bigint NULL REFERENCES "accounts_mahasiswa" ("id") DEFERRABLE INITIALLY DEFERRED,
        "status" varchar(20) NULL,
        CONSTRAINT "unique_krs_mahasiswa_tahun_ajaran_semester" UNIQUE ("mahasiswa_id", "tahun_ajaran", "semester")
    );

CREATE TABLE
    "academic_kurikulum" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "tahun" varchar(10) NULL,
        "semester" varchar(10) NULL,
        "program_studi_id" bigint NULL REFERENCES "academic_prodi" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "academic_kurikulummatakuliah" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "sifat" varchar(20) NULL,
        "kurikulum_id" bigint NULL REFERENCES "academic_kurikulum" ("id") DEFERRABLE INITIALLY DEFERRED,
        "mata_kuliah_id" bigint NULL REFERENCES "academic_matakuliah" ("id") DEFERRABLE INITIALLY DEFERRED,
        CONSTRAINT "unique_kurikulum_mata_kuliah" UNIQUE ("kurikulum_id", "mata_kuliah_id")
    );

CREATE TABLE
    "academic_matakuliah" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "kode" varchar(20) NULL UNIQUE,
        "nama" varchar(100) NULL,
        "sks" integer NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "semester" integer NULL
    );

CREATE TABLE
    "academic_nilai" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "nilai_angka" real NULL,
        "nilai_huruf" varchar(10) NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "detail_krs_id" bigint NULL UNIQUE REFERENCES "academic_detailkrs" ("id") DEFERRABLE INITIALLY DEFERRED,
        CONSTRAINT "nilai_angka_antara_0_dan_100" CHECK (
            (
                "nilai_angka" >= 0.0
                AND "nilai_angka" <= 100.0
            )
        )
    );

CREATE TABLE
    "academic_nilaikomponen" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "nilai" real NULL,
        "komponen_nilai_id" bigint NULL REFERENCES "academic_komponennilai" ("id") DEFERRABLE INITIALLY DEFERRED,
        "nilai_id_id" bigint NULL REFERENCES "academic_nilai" ("id") DEFERRABLE INITIALLY DEFERRED,
        CONSTRAINT "nilai_antara_0_dan_100" CHECK (
            (
                "nilai" >= 0.0
                AND "nilai" <= 100.0
            )
        ),
        CONSTRAINT "unique_nilai_komponen" UNIQUE ("nilai_id_id", "komponen_nilai_id")
    );

CREATE TABLE
    "academic_penawarankrs" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "kuota" integer NULL,
        "created" datetime NOT NULL,
        "updated" datetime NOT NULL,
        "kelas_id" bigint NULL REFERENCES "academic_kelas" ("id") DEFERRABLE INITIALLY DEFERRED,
        "periode_krs_id" bigint NULL REFERENCES "academic_periodekrs" ("id") DEFERRABLE INITIALLY DEFERRED,
        CONSTRAINT "unique_periode_krs_kelas" UNIQUE ("periode_krs_id", "kelas_id")
    );

CREATE TABLE
    "academic_periodekrs" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "semester" varchar(10) NULL,
        "tanggal_mulai" date NULL,
        "tanggal_selesai" date NULL,
        "status" varchar(20) NULL,
        "created" datetime NOT NULL,
        "updated" datetime NOT NULL,
        "tahun_ajaran" varchar(10) NULL,
        CONSTRAINT "tanggal_mulai_lebih_kecil_dari_tanggal_selesai" CHECK (
            (
                "tanggal_mulai" IS NULL
                OR "tanggal_selesai" IS NULL
                OR "tanggal_selesai" >= ("tanggal_mulai")
            )
        ),
        CONSTRAINT "unique_tahun_ajaran_semester" UNIQUE ("tahun_ajaran", "semester")
    );

CREATE TABLE
    "academic_prodi" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "kode" varchar(10) NULL UNIQUE,
        "nama" varchar(100) NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "fakultas_id" bigint NULL REFERENCES "academic_fakultas" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "accounts_dosen" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "nama" varchar(100) NULL,
        "email" varchar(254) NULL,
        "no_hp" varchar(20) NULL,
        "alamat" text NULL,
        "tempat_lahir" varchar(100) NULL,
        "tanggal_lahir" date NULL,
        "jenis_kelamin" varchar(100) NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "user_id" integer NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "nip" varchar(10) NULL UNIQUE
    );

CREATE TABLE
    "accounts_mahasiswa" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "nama" varchar(100) NULL,
        "email" varchar(254) NULL,
        "no_hp" varchar(20) NULL,
        "alamat" text NULL,
        "tempat_lahir" varchar(100) NULL,
        "tanggal_lahir" date NULL,
        "jenis_kelamin" varchar(100) NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "status" varchar(20) NULL,
        "prodi_id" bigint NULL REFERENCES "academic_prodi" ("id") DEFERRABLE INITIALLY DEFERRED,
        "user_id" integer NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "nim" varchar(10) NULL UNIQUE
    );

CREATE TABLE
    "auth_group" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" varchar(150) NOT NULL UNIQUE
    );

CREATE TABLE
    "auth_group_permissions" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
        "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "auth_permission" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
        "codename" varchar(100) NOT NULL,
        "name" varchar(255) NOT NULL
    );

CREATE TABLE
    "auth_user" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "password" varchar(128) NOT NULL,
        "last_login" datetime NULL,
        "is_superuser" bool NOT NULL,
        "username" varchar(150) NOT NULL UNIQUE,
        "last_name" varchar(150) NOT NULL,
        "email" varchar(254) NOT NULL,
        "is_staff" bool NOT NULL,
        "is_active" bool NOT NULL,
        "date_joined" datetime NOT NULL,
        "first_name" varchar(150) NOT NULL
    );

CREATE TABLE
    "auth_user_groups" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "auth_user_user_permissions" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "django_admin_log" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "object_id" text NULL,
        "object_repr" varchar(200) NOT NULL,
        "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0),
        "change_message" text NOT NULL,
        "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "action_time" datetime NOT NULL
    );

CREATE TABLE
    "django_content_type" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "app_label" varchar(100) NOT NULL,
        "model" varchar(100) NOT NULL
    );

CREATE TABLE
    "django_migrations" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "app" varchar(255) NOT NULL,
        "name" varchar(255) NOT NULL,
        "applied" datetime NOT NULL
    );

CREATE TABLE
    "django_session" (
        "session_key" varchar(40) NOT NULL PRIMARY KEY,
        "session_data" text NOT NULL,
        "expire_date" datetime NOT NULL
    );

CREATE TABLE
    "penugasan_pengumpulantugas" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "tanggal_kirim" datetime NOT NULL,
        "file_url" varchar(200) NOT NULL,
        "catatan" text NOT NULL,
        "status" varchar(15) NOT NULL,
        "penugasan_id" bigint NOT NULL REFERENCES "penugasan_penugasan" ("id") DEFERRABLE INITIALLY DEFERRED,
        "mahasiswa_id" bigint NULL REFERENCES "accounts_mahasiswa" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    "penugasan_penugasan" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "judul" varchar(255) NOT NULL,
        "deskripsi" text NOT NULL,
        "tanggal_dibuat" datetime NOT NULL,
        "tanggal_dibuka" datetime NOT NULL,
        "batas_pengumpulan" datetime NOT NULL,
        "jenis" varchar(10) NOT NULL,
        "file_url" varchar(200) NOT NULL,
        "kelas_id" bigint NOT NULL REFERENCES "academic_kelas" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE
    sqlite_sequence (name, seq);