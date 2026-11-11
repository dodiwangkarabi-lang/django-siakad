def nilai_to_point(nilai: int, bobot: int) -> int:
    hasil = (nilai / 100) * bobot
    return min(int(round(hasil)), bobot)

def total_point(kumpulan_nilai: list) -> int:
    return sum(
        nilai_to_point(item["nilai"], item["bobot"])
        for item in kumpulan_nilai
    )

def total_bobot(kumpulan_nilai: list) -> int:
    return sum(
        item["bobot"]
        for item in kumpulan_nilai
    )

def nilai_akhir(total_point: int, total_bobot: int) -> int:
    if total_bobot <= 0:
        return 0

    hasil = (total_point / total_bobot) * 100
    return min(max(int(round(hasil)), 0), 100)