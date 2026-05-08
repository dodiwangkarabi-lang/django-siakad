from academic.constants import *
from academic.models import MataKuliah
from accounts.models import Mahasiswa
import pandas as pd
import pickle

def split_ttl(ttl_value):
    """
    memisahkan kolom yang berisi nilai tanggal lahir dan tempat lahir jadi 2 kolom

    Args:
        ttl_value (str): nilai tanggal lahir dan tempat lahir

    Returns:
        _type_: _description_
        
    Example:
        >>> split_ttl("JAKARTA, 01 JANUARI 2000")
        >>> ["JAKARTA", "2000-01-01"]
        
    """
    try:
        if pd.isna(ttl_value):
            return pd.Series([None, None])

        # pisahkan tempat dan tanggal
        parts = ttl_value.split(",")
        tempat = parts[0].strip()

        tanggal_str = parts[1].strip().upper()

        # pecah tanggal
        tgl, bulan, tahun = tanggal_str.split()

        bulan_angka = BULAN_MAP.get(bulan, 1)

        tanggal = pd.Timestamp(
            year=int(tahun),
            month=bulan_angka,
            day=int(tgl)
        )

        return pd.Series([tempat, tanggal])

    except Exception:
        return pd.Series([None, None])
    
def queryset_to_df(queryset, fields=None):
    """
    Convert Django QuerySet ke pandas DataFrame
    
    Args:
        queryset (QuerySet): QuerySet Django
        fields (list, optional): List field yang ingin diambil. Defaults to None.
    
    Returns:
        pandas DataFrame
    
    Example:
        >>> queryset_to_df(Mahasiswa.objects.all(), fields=["nim", "nama"])
        >>> pandas DataFrame
    """
    if fields:
        data = queryset.values(*fields)
    else:
        data = queryset.values()

    return pd.DataFrame(list(data))


# -----------------------------------

def validate_to_db(form_data):
    errors = {}

    daftar_nim = form_data.get("daftar_nim", [])
    daftar_kode = form_data.get("daftar_kode_mata_kuliah", [])

    nim_exist = set(
        Mahasiswa.objects.filter(nim__in=daftar_nim)
        .values_list("nim", flat=True)
    )

    kode_exist = set(
        MataKuliah.objects.filter(kode__in=daftar_kode)
        .values_list("kode", flat=True)
    )

    nim_invalid = set(daftar_nim) - nim_exist
    kode_invalid = set(daftar_kode) - kode_exist

    if nim_invalid:
        errors["daftar_nim"] = list(nim_invalid)

    if kode_invalid:
        errors["daftar_kode_mata_kuliah"] = list(kode_invalid)

    return errors

def validate_basic(form_data):
    errors = {}

    if not form_data.get("daftar_nim"):
        errors["daftar_nim"] = "Tidak boleh kosong"

    if not form_data.get("daftar_kode_mata_kuliah"):
        errors["daftar_kode_mata_kuliah"] = "Tidak boleh kosong"

    return errors

def validate_items(form_data):
    errors = {
        "daftar_nim": [],
        "daftar_kode_mata_kuliah": []
    }

    for nim in form_data.get("daftar_nim", []):
        if not nim.isdigit():
            errors["daftar_nim"].append(f"{nim} bukan angka")

    for kode in form_data.get("daftar_kode_mata_kuliah", []):
        if len(kode) < 5:
            errors["daftar_kode_mata_kuliah"].append(f"{kode} tidak valid")

    return errors

def validate_form_data(form_data):
    errors = {}

    # basic
    errors.update(validate_basic(form_data))

    # item
    item_errors = validate_items(form_data)

    for key, val in item_errors.items():
        if val:
            errors[key] = val

    # db
    db_errors = validate_to_db(form_data)
    errors.update(db_errors)

    return errors

class ParquetService:
    @staticmethod
    def simpan(data, file_path):
        data.to_parquet(file_path, engine="pyarrow", compression="snappy")
    
    @staticmethod
    def load(file_path):
        return pd.read_parquet(file_path)
    
class PickleService:
    @staticmethod
    def simpan(data, file_path):
        with open(file_path, "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def load(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
        

def hitung_total_sks(daftar_kode_mata_kuliah):
    """
    Hitung jumlah sks otomatis

    Args:
        daftar_kode_mata_kuliah (list): kumpulan kode mata kuliah

    Returns:
        int: total sks
        
    Example:
        >>> hitung_sks(["A001", "A002", "A003"])
    """
    return sum(MataKuliah.objects.filter(kode__in=daftar_kode_mata_kuliah).values_list("sks", flat=True))