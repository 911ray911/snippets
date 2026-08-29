# Snippets — Kode Tutorial Ray Soesanto

Kumpulan snippet kode dari tulisan & tutorial Ray Soesanto (Teknik Industri, Universitas Telkom).

## Daftar

### contoh_mm1.py
Model antrean M/M/1 dengan SimPy — tutorial Medium: "Simulasi Kejadian Diskrit untuk Teknik Industri".

- Kedatangan Poisson (laju 4/jam), layanan eksponensial (laju 5/jam), 1 server
- Konsep: Environment, Process, Event, Resource
- Output: jumlah part dilayani, waktu tunggu rata-rata, utilisasi

```bash
pip install simpy==4.1.2
python contoh_mm1.py
```

### contoh_mmc.py
Lanjutan: antrean multi-server M/M/c (c mesin paralel).

- 3 server paralel, laju kedatangan 8/jam, laju layanan 3/jam per server (rho 0.889)
- Bandingkan waktu tunggu vs 1 mesin cepat

```bash
python contoh_mmc.py
```

### contoh_breakdown.py
Lanjutan: mesin dengan kerusakan (interrupt).

- `simpy.Interrupt` saat mesin rusak di tengah proses, item diulang, MTTR delay
- MTBF 50, MTTR 5, waktu proses 4

```bash
python contoh_breakdown.py
```

## Lisensi
MIT — silakan pakai, modifikasi, sebarkan.
