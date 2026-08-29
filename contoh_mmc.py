"""
contoh-02-mmc.py - Model antrean M/M/c dengan SimPy.
Buku: Simulasi Kejadian Diskrit dengan Python dan LLM
"""
import simpy
import random
import statistics


class AntreanMMc:
    """M/M/c: kedatangan Poisson, layanan eksponensial, c server paralel."""

    def __init__(self, env, laju_kedatangan, laju_layanan, jumlah_server):
        self.env = env
        self.laju_kedatangan = laju_kedatangan
        self.laju_layanan = laju_layanan
        self.server = simpy.Resource(env, capacity=jumlah_server)
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


def jalankan(laju_kedatangan=8.0, laju_layanan=3.0, jumlah_server=3, durasi=1000, seed=7):
    random.seed(seed)
    env = simpy.Environment()
    model = AntreanMMc(env, laju_kedatangan, laju_layanan, jumlah_server)
    env.process(model.kedatangan())
    env.run(until=durasi)
    n = len(model.waktu_tunggu)
    rho = laju_kedatangan / (jumlah_server * laju_layanan)
    return {
        "mulai_dilayani": n,
        "selesai_dilayani": model.selesai,
        "waktu_tunggu_rata": statistics.mean(model.waktu_tunggu) if n else 0,
        "intensitas_trafik_rho": rho,
    }


if __name__ == "__main__":
    hasil = jalankan()
    print(f"Pelanggan mulai dilayani: {hasil['mulai_dilayani']}")
    print(f"Pelanggan selesai dilayani: {hasil['selesai_dilayani']}")
    print(f"Waktu tunggu rata-rata: {hasil['waktu_tunggu_rata']:.3f} satuan waktu")
    print(f"Intensitas trafik rho: {hasil['intensitas_trafik_rho']:.3f}")
