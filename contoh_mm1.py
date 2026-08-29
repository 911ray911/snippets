"""
contoh-02-mm1.py - Model antrean M/M/1 dengan SimPy.
Buku: Simulasi Kejadian Diskrit dengan Python dan LLM
"""
import simpy
import random
import statistics

class AntreanMM1:
    """Model M/M/1: kedatangan Poisson, layanan eksponensial, 1 server."""

    def __init__(self, env, laju_kedatangan, laju_layanan):
        self.env = env
        self.laju_kedatangan = laju_kedatangan
        self.laju_layanan = laju_layanan
        self.server = simpy.Resource(env, capacity=1)
        self.waktu_tunggu = []
        self.selesai = 0

    def layani(self, pelanggan_id):
        tiba = self.env.now
        with self.server.request() as req:
            yield req
            tunggu = self.env.now - tiba
            self.waktu_tunggu.append(tunggu)
            yield self.env.timeout(random.expovariate(self.laju_layanan))
            self.selesai += 1

    def kedatangan(self):
        i = 0
        while True:
            yield self.env.timeout(random.expovariate(self.laju_kedatangan))
            i += 1
            self.env.process(self.layani(i))


def jalankan(laju_kedatangan=4.0, laju_layanan=5.0, durasi=1000, seed=42):
    random.seed(seed)
    env = simpy.Environment()
    model = AntreanMM1(env, laju_kedatangan, laju_layanan)
    env.process(model.kedatangan())
    env.run(until=durasi)
    n = len(model.waktu_tunggu)
    return {
        "mulai_dilayani": n,
        "selesai_dilayani": model.selesai,
        "waktu_tunggu_rata": statistics.mean(model.waktu_tunggu) if n else 0,
        "utilisasi": laju_kedatangan / laju_layanan,
    }


if __name__ == "__main__":
    hasil = jalankan()
    print(f"Pelanggan mulai dilayani: {hasil['mulai_dilayani']}")
    print(f"Pelanggan selesai dilayani: {hasil['selesai_dilayani']}")
    print(f"Waktu tunggu rata-rata: {hasil['waktu_tunggu_rata']:.3f} satuan waktu")
    print(f"Utilisasi server (teori): {hasil['utilisasi']:.3f}")
