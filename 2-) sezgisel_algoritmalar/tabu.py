
import random


class TabuSearch:
    def __init__(
        self,
        islem_sayisi,
        maliyet_fonksiyonu=lambda x: x[0] ** 2 + 2 * x[0] * x[1] - x[1] ** 3,
        tabu_size=20,
        komsu_sayisi=30,
        iterasyon_sayisi=300,
        alt_sinir=-10.0,
        ust_sinir=10.0,
        komsu_alt_delta=-0.5,
        komsu_ust_delta=0.5,
        random_seed=42,
    ):
        self.islem_sayisi = islem_sayisi
        self.maliyet_fonksiyonu = maliyet_fonksiyonu or self.varsayilan_maliyet
        self.tabu_size = tabu_size
        self.komsu_sayisi = komsu_sayisi
        self.iterasyon_sayisi = iterasyon_sayisi
        self.alt_sinir = alt_sinir
        self.ust_sinir = ust_sinir
        self.komsu_alt_delta = komsu_alt_delta
        self.komsu_ust_delta = komsu_ust_delta

        self.random = random.Random(random_seed)
        self.tabu_list = []

    def varsayilan_maliyet(self, cozum):
        if len(cozum) != 2:
            raise ValueError("Bu varsayilan maliyet fonksiyonu icin islem_sayisi 2 olmalidir.")

        x1, x2 = cozum
        return x1 ** 2 + 2 * x1 * x2 - x2 ** 3

    def random_cozum(self):
        return [self.random.uniform(self.alt_sinir, self.ust_sinir) for _ in range(self.islem_sayisi)]

    def komsu_uret(self, cozum):
        index = self.random.randrange(self.islem_sayisi)
        delta = self.random.uniform(self.komsu_alt_delta, self.komsu_ust_delta)
        komsu = cozum.copy()
        yeni_deger = komsu[index] + delta
        komsu[index] = min(self.ust_sinir, max(self.alt_sinir, yeni_deger))

        # Hareketi (degisen indeks, yon) olarak sakliyoruz.
        move = (index, 1 if delta >= 0 else -1)
        return komsu, move

    def komsu_listesi_uret(self, cozum):
        return [self.komsu_uret(cozum) for _ in range(self.komsu_sayisi)]

    def add_move(self, move):
        self.tabu_list.append(move)
        if len(self.tabu_list) > self.tabu_size:
            self.tabu_list.pop(0)

    def is_tabu(self, move):
        return move in self.tabu_list

    def optimize(self, raporlama=False, rapor_araligi=25):
        mevcut_cozum = self.random_cozum()
        mevcut_maliyet = self.maliyet_fonksiyonu(mevcut_cozum)

        en_iyi_cozum = mevcut_cozum.copy()
        en_iyi_maliyet = mevcut_maliyet
        maliyet_gecmisi = [en_iyi_maliyet]
        rapor = []

        if raporlama:
            mesaj = f"Baslangic | mevcut={mevcut_maliyet:.6f} | en_iyi={en_iyi_maliyet:.6f}"
            print(mesaj)
            rapor.append(mesaj)

        for i in range(self.iterasyon_sayisi):
            adaylar = self.komsu_listesi_uret(mevcut_cozum)

            secilen_cozum = None
            secilen_maliyet = float("inf")
            secilen_move = None

            for aday_cozum, move in adaylar:
                aday_maliyet = self.maliyet_fonksiyonu(aday_cozum)

                # Aspiration: tabu hamlesi global en iyiyi iyilestiriyorsa kabul edilir.
                if self.is_tabu(move) and aday_maliyet >= en_iyi_maliyet:
                    continue

                if aday_maliyet < secilen_maliyet:
                    secilen_cozum = aday_cozum
                    secilen_maliyet = aday_maliyet
                    secilen_move = move

            if secilen_cozum is None:
                # Tum hamleler tabu ise rastgele bir komsuyla devam et.
                secilen_cozum, secilen_move = self.komsu_uret(mevcut_cozum)
                secilen_maliyet = self.maliyet_fonksiyonu(secilen_cozum)

            mevcut_cozum = secilen_cozum
            mevcut_maliyet = secilen_maliyet
            self.add_move(secilen_move)

            if mevcut_maliyet < en_iyi_maliyet:
                en_iyi_cozum = mevcut_cozum.copy()
                en_iyi_maliyet = mevcut_maliyet

            maliyet_gecmisi.append(en_iyi_maliyet)

            if raporlama and ((i + 1) % rapor_araligi == 0 or i == self.iterasyon_sayisi - 1):
                mesaj = (
                    f"Iterasyon {i + 1:4d} | mevcut={mevcut_maliyet:.6f} | "
                    f"en_iyi={en_iyi_maliyet:.6f} | tabu_uzunluk={len(self.tabu_list)}"
                )
                print(mesaj)
                rapor.append(mesaj)

        if raporlama:
            mesaj = f"Bitis    | en_iyi={en_iyi_maliyet:.6f} | cozum={en_iyi_cozum}"
            print(mesaj)
            rapor.append(mesaj)

        return {
            "en_iyi_cozum": en_iyi_cozum,
            "en_iyi_maliyet": en_iyi_maliyet,
            "maliyet_gecmisi": maliyet_gecmisi,
            "rapor": rapor,
        }


if __name__ == "__main__":
    def amac_fonksiyonu(cozum):
        x1, x2 = cozum
        return x1 ** 2 + 2 * x1 * x2 - x2 ** 3

    optimizer = TabuSearch(
        islem_sayisi=2,
        maliyet_fonksiyonu=amac_fonksiyonu,
        tabu_size=20,
        komsu_sayisi=40,
        iterasyon_sayisi=300,
        random_seed=42,
    )
    sonuc = optimizer.optimize(raporlama=True, rapor_araligi=50)
    print("En Iyi Cozum:", sonuc["en_iyi_cozum"])
    print("En Iyi Maliyet:", sonuc["en_iyi_maliyet"])