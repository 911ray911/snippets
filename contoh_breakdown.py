"""
contoh-02-breakdown.py - Mesin dengan kerusakan (interrupt) di SimPy.
Buku: Simulasi Kejadian Diskrit dengan Python dan LLM
"""
import simpy
import random


def kerusakan(env, mesin_proses, mtbf):
    """Generator kerusakan: timeout eksponensial, lalu interrupt mesin."""
    yield env.timeout(random.expovariate(1 / mtbf))
    if mesin_proses.is_alive:
        mesin_proses.interrupt()


def mesin(env, nama, waktu_proses, mtbf, mttr):
    """Proses mesin: proses item, bisa di-interrupt kerusakan, lalu perbaiki."""
    while True:
        try:
            yield env.timeout(waktu_proses)
        except simpy.Interrupt:
            # Kerusakan terjadi saat mesin memproses item.
            # Item yang sedang diproses "hilang" (harus diulang), mesin rusak.
            yield env.timeout(mttr)
            # Setelah diperbaiki, lanjut memproses item berikutnya (loop).


def jalankan(durasi=2000, seed=11):
    random.seed(seed)
    env = simpy.Environment()
    proses_mesin = env.process(
        mesin(env, "Mesin-1", waktu_proses=4.0, mtbf=50.0, mttr=5.0)
    )
    env.process(kerusakan(env, proses_mesin, mtbf=50.0))
    env.run(until=durasi)
    return {"durasi": durasi}


if __name__ == "__main__":
    hasil = jalankan()
    print(f"Simulasi mesin dengan kerusakan selesai ({hasil['durasi']} satuan waktu).")
