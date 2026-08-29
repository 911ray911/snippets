"""
war_tiket.py - War tiket konser: human vs bot calo (antrean M/M/c, SimPy).
Kasus ilustrasi: King Nassar "Lost in the Jungle", Istora Senayan, 7 Nov 2026.
Asumsi eksplisit: 7.000 tiket, kedatangan 500 pembeli/menit, human ~2 dtk,
bot ~0,5 dtk (4x lebih cepat), 40% trafik bot. Bandingkan dengan dan tanpa bot.
"""
import simpy
import random
import statistics

HUMAN_LAMA = 2.0    # detik isi formulir + bayar (manusia)
BOT_LAMA = 0.5      # detik (bot, 4x lebih cepat)


class WarTiket:
    """Antrean pembelian tiket: human vs bot berebut slot server."""

    def __init__(self, env, jumlah_server, kapasitas):
        self.env = env
        self.server = simpy.Resource(env, capacity=jumlah_server)
        self.kapasitas = kapasitas
        self.tiket = 0
        self.dapat = {"human": 0, "bot": 0}
        self.gagal = {"human": 0, "bot": 0}
        self.waktu_tunggu = []

    def beli(self, jenis, lama):
        tiba = self.env.now
        if self.tiket >= self.kapasitas:
            self.gagal[jenis] += 1
            return
        with self.server.request() as req:
            yield req
            self.waktu_tunggu.append(self.env.now - tiba)
            yield self.env.timeout(lama)
            if self.tiket < self.kapasitas:
                self.tiket += 1
                self.dapat[jenis] += 1
            else:
                self.gagal[jenis] += 1


def jalankan(bot_aktif, seed=7, laju=500.0, jumlah_server=100, kapasitas=7000,
             durasi=600.0):
    """bot_aktif True = 40% trafik bot; False = semua human."""
    random.seed(seed)
    env = simpy.Environment()
    m = WarTiket(env, jumlah_server, kapasitas)
    proporsi_bot = 0.40 if bot_aktif else 0.0

    def kedatangan():
        i = 0
        while i < 30000:  # batas event agar simulasi cepat
            yield env.timeout(random.expovariate(laju))
            i += 1
            if random.random() < proporsi_bot:
                env.process(m.beli("bot", BOT_LAMA))
            else:
                env.process(m.beli("human", HUMAN_LAMA))

    env.process(kedatangan())
    env.run(until=durasi)
    return m


if __name__ == "__main__":
    for bot in (True, False):
        m = jalankan(bot)
        wt = statistics.mean(m.waktu_tunggu) if m.waktu_tunggu else 0
        label = "DENGAN bot (40%)" if bot else "TANPA bot"
        print(f"[{label}] tiket {m.tiket} | human {m.dapat['human']} "
              f"| bot {m.dapat['bot']} | gagal {m.gagal['human']}/{m.gagal['bot']} "
              f"| WT rata {wt:.0f} dtk")
