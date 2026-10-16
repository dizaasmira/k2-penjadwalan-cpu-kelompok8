#!/usr/bin/env python3
"""
Simulator Penjadwalan CPU - Tugas K-2 Sistem Operasi (Kelas D)
Algoritma: FCFS, SJF (non-preemptive), SRTF, Priority (NP & P), Round Robin

Format data proses: (nama, arrival, burst, prioritas)
Prioritas: angka kecil = prioritas tinggi.
Hasil tiap algoritma berupa "timeline": list (nama, mulai, selesai).
"""

DATASET = [
    ("P1", 0, 5, 2),
    ("P2", 2, 3, 1),
    ("P3", 3, 10, 4),
    ("P4", 4, 4, 2),
    ("P5", 7, 6, 3),
]


# ---------------------------------------------------------------
# Bantu: gabungkan potongan berurutan milik proses yang sama
# ---------------------------------------------------------------
def gabung(timeline):
    hasil = []
    for nama, s, e in timeline:
        if hasil and hasil[-1][0] == nama and hasil[-1][2] == s:
            hasil[-1] = (nama, hasil[-1][1], e)
        else:
            hasil.append((nama, s, e))
    return hasil


# ---------------------------------------------------------------
# 1) Algoritma NON-PREEMPTIVE (FCFS, SJF, Priority NP)
#    Cukup beda di "kunci" pemilihan proses berikutnya.
# ---------------------------------------------------------------
def non_preemptive(procs, kunci):
    sisa = list(procs)
    t, timeline = 0, []
    while sisa:
        siap = [p for p in sisa if p[1] <= t]
        if not siap:                       # CPU idle, loncat ke kedatangan berikutnya
            t = min(p[1] for p in sisa)
            continue
        p = min(siap, key=kunci)           # pilih yang kuncinya paling kecil
        timeline.append((p[0], t, t + p[2]))
        t += p[2]
        sisa.remove(p)
    return timeline


def fcfs(procs):
    return non_preemptive(procs, lambda p: (p[1], p[0]))          # arrival


def sjf(procs):
    return non_preemptive(procs, lambda p: (p[2], p[1], p[0]))    # burst terkecil


def priority_np(procs):
    return non_preemptive(procs, lambda p: (p[3], p[1], p[0]))    # prioritas terkecil


# ---------------------------------------------------------------
# 2) Algoritma PREEMPTIVE (SRTF, Priority P): cek ulang tiap 1 satuan waktu
# ---------------------------------------------------------------
def preemptive(procs, kunci):
    sisa = {p[0]: p[2] for p in procs}     # sisa burst tiap proses
    data = {p[0]: p for p in procs}
    t, timeline = 0, []
    while any(v > 0 for v in sisa.values()):
        siap = [n for n in sisa if sisa[n] > 0 and data[n][1] <= t]
        if not siap:
            t += 1
            continue
        n = min(siap, key=lambda x: kunci(data[x], sisa[x]))
        timeline.append((n, t, t + 1))
        sisa[n] -= 1
        t += 1
    return gabung(timeline)


def srtf(procs):
    return preemptive(procs, lambda p, sisa: (sisa, p[1], p[0]))


def priority_p(procs):
    return preemptive(procs, lambda p, sisa: (p[3], p[1], p[0]))


# ---------------------------------------------------------------
# 3) Round Robin
#    Aturan: proses yang BARU DATANG masuk antrean lebih dulu
#    daripada proses yang baru saja habis kuantum-nya.
# ---------------------------------------------------------------
def round_robin(procs, quantum):
    urut = sorted(procs, key=lambda p: (p[1], p[0]))
    sisa = {p[0]: p[2] for p in procs}
    antrean, sudah_masuk = [], set()
    t, timeline = 0, []

    def masukkan(waktu):
        for p in urut:
            if p[1] <= waktu and p[0] not in sudah_masuk:
                antrean.append(p[0])
                sudah_masuk.add(p[0])

    while any(v > 0 for v in sisa.values()):
        masukkan(t)
        if not antrean:
            t = min(p[1] for p in urut if p[0] not in sudah_masuk)
            continue
        n = antrean.pop(0)
        jalan = min(quantum, sisa[n])
        timeline.append((n, t, t + jalan))
        t += jalan
        sisa[n] -= jalan
        masukkan(t)                         # pendatang baru dulu...
        if sisa[n] > 0:
            antrean.append(n)               # ...baru proses yang belum selesai
    return timeline


# ---------------------------------------------------------------
# Hitung metrik: CT, TAT, WT, RT
# ---------------------------------------------------------------
def hitung_metrik(procs, timeline):
    hasil = {}
    for nama, arrival, burst, _ in procs:
        potongan = [x for x in timeline if x[0] == nama]
        mulai_pertama = min(x[1] for x in potongan)
        selesai = max(x[2] for x in potongan)
        tat = selesai - arrival
        hasil[nama] = {
            "CT": selesai,
            "TAT": tat,
            "WT": tat - burst,
            "RT": mulai_pertama - arrival,
        }
    return hasil


def cetak_gantt(timeline):
    bar, skala = "|", "0"
    for nama, s, e in timeline:
        lebar = max(len(nama) + 2, (e - s) * 2)
        bar += nama.center(lebar) + "|"
        skala += str(e).rjust(lebar + 1)
    print("Gantt chart:")
    print(bar)
    print(skala)


def cetak_hasil(judul, procs, timeline):
    print("=" * 60)
    print(judul)
    print("=" * 60)
    cetak_gantt(timeline)
    m = hitung_metrik(procs, timeline)
    print(f"\n{'Proses':<8}{'CT':>5}{'TAT':>6}{'WT':>5}{'RT':>5}")
    for nama, _, _, _ in procs:
        d = m[nama]
        print(f"{nama:<8}{d['CT']:>5}{d['TAT']:>6}{d['WT']:>5}{d['RT']:>5}")
    n = len(procs)
    rata = {k: sum(m[x][k] for x in m) / n for k in ("TAT", "WT", "RT")}
    print(f"\nRata-rata  WT={rata['WT']:.2f}  TAT={rata['TAT']:.2f}  RT={rata['RT']:.2f}\n")
    return rata


if __name__ == "__main__":
    skenario = [
        ("FCFS", fcfs(DATASET)),
        ("SJF (non-preemptive)", sjf(DATASET)),
        ("SRTF (SJF preemptive)", srtf(DATASET)),
        ("Priority (non-preemptive)", priority_np(DATASET)),
        ("Priority (preemptive)", priority_p(DATASET)),
        ("Round Robin q=4", round_robin(DATASET, 4)),
        ("Round Robin q=6", round_robin(DATASET, 6)),
    ]
    ringkasan = []
    for judul, tl in skenario:
        ringkasan.append((judul, cetak_hasil(judul, DATASET, tl)))

    print("=" * 60)
    print("TABEL PERBANDINGAN")
    print("=" * 60)
    print(f"{'Algoritma':<28}{'Avg WT':>8}{'Avg TAT':>9}{'Avg RT':>8}")
    for judul, r in ringkasan:
        print(f"{judul:<28}{r['WT']:>8.2f}{r['TAT']:>9.2f}{r['RT']:>8.2f}")
