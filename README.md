# K-2 Simulasi dan Evaluasi Algoritma Penjadwalan CPU

Sistem Operasi (USA-WP2260110) · Kelas D · Cloud dan Layanan Digital UMKM

Simulator sederhana untuk membandingkan algoritma penjadwalan CPU pada dataset kelas
(konteks: pemrosesan pesanan, verifikasi pembayaran, dan notifikasi saat flash sale).

Algoritma yang disimulasikan:

- FCFS
- SJF (non-preemptive)
- SRTF (SJF preemptive)
- Priority (non-preemptive dan preemptive)
- Round Robin (quantum 4 dan 6)

## Dataset

Format: (arrival, burst, prioritas). Angka prioritas kecil berarti prioritas tinggi.

| Proses | Arrival | Burst | Prioritas |
|--------|---------|-------|-----------|
| P1     | 0       | 5     | 2         |
| P2     | 2       | 3     | 1         |
| P3     | 3       | 10    | 4         |
| P4     | 4       | 4     | 2         |
| P5     | 7       | 6     | 3         |

## Cara menjalankan

Kebutuhan: Python 3 (tanpa pustaka tambahan).

```bash
cd kode
python3 simulator_cpu.py
```

Untuk menyimpan keluaran ke berkas:

```bash
python3 simulator_cpu.py | tee ../hasil/hasil_simulasi.txt
```

Keluaran berisi Gantt chart teks, tabel CT, TAT, WT, dan RT per proses, serta tabel
perbandingan di akhir.

## Hasil ringkas

| Algoritma                 | Rata-rata WT | Rata-rata TAT | Rata-rata RT |
|---------------------------|--------------|---------------|--------------|
| FCFS                      | 7.40         | 13.00         | 7.40         |
| SJF (non-preemptive)      | 5.40         | 11.00         | 5.40         |
| SRTF (SJF preemptive)     | 5.40         | 11.00         | 5.40         |
| Priority (non-preemptive) | 5.40         | 11.00         | 5.40         |
| Priority (preemptive)     | 5.40         | 11.00         | 4.80         |
| Round Robin q=4           | 9.60         | 15.20         | 4.40         |
| Round Robin q=6           | 7.80         | 13.40         | 5.80         |

Keterangan: WT = waiting time, TAT = turnaround time, RT = response time.

## Aturan yang dipakai

- Satu CPU, tanpa I/O, dan waktu context switch dianggap nol.
- SJF dan Priority: bila seri, proses yang datang lebih awal dipilih.
- SRTF: bila sisa burst proses berjalan sama dengan burst proses baru, proses berjalan
  tidak dipotong.
- Round Robin: proses yang baru datang masuk antrean lebih dulu daripada proses yang
  baru habis kuantum.

## Struktur repositori

```
.
├── README.md
├── kode/
│   └── simulator_cpu.py        # simulator
├── hasil/
│   └── hasil_simulasi.txt      # keluaran simulator
└── log/
    └── sesi_k2_bersih.txt      # log sesi terminal
```

## Cara kerja kode

- `non_preemptive()` dipakai FCFS, SJF, dan Priority NP. Perbedaannya hanya pada kunci
  pemilihan proses (arrival, burst, atau prioritas).
- `preemptive()` dipakai SRTF dan Priority P. Pilihan diperiksa ulang tiap satu satuan
  waktu sehingga pemotongan proses terjadi otomatis.
- `round_robin()` memakai antrean dengan aturan pendatang baru masuk lebih dulu.
- `hitung_metrik()` menghitung CT, TAT, WT, dan RT dari Gantt chart.
