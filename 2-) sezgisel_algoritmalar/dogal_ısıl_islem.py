import math
import random


class DogalIsilIslem:
    def __init__(
        self,
        islem_sayisi,
        maliyet_fonksiyonu=None,
        alt_sinir=-10.0,
        ust_sinir=10.0,
        baslangic_sicakligi=400.0,
        sogutma_katsayisi=0.95,
        min_sicaklik=0.001,
        komsu_alt_delta=-0.5,
        komsu_ust_delta=0.5,
        random_seed=None,
    ):
        self.islem_sayisi = islem_sayisi
        self.islemler = []

        self.alt_sinir = alt_sinir
        self.ust_sinir = ust_sinir
        self.baslangic_sicakligi = baslangic_sicakligi
        self.sogutma_katsayisi = sogutma_katsayisi
        self.min_sicaklik = min_sicaklik
        self.komsu_alt_delta = komsu_alt_delta
        self.komsu_ust_delta = komsu_ust_delta

        self.maliyet_fonksiyonu = maliyet_fonksiyonu or self.varsayilan_maliyet
        self.random = random.Random(random_seed)

    def random_islem(self):
        return self.random.uniform(self.alt_sinir, self.ust_sinir)

    def initzalite(self):
        self.islemler = [self.random_islem() for _ in range(self.islem_sayisi)]
        return self.islemler

    def initialize(self):
        return self.initzalite()

    def varsayilan_maliyet(self, cozum):
        if len(cozum) != 2:
            raise ValueError("Bu varsayilan maliyet fonksiyonu icin islem_sayisi 2 olmalidir.")

        x1, x2 = cozum
        return x1 ** 2 + 2 * x1 * x2 - x2 ** 3

    def komsu_uret(self, cozum):
        komsu = cozum.copy()
        index = self.random.randrange(self.islem_sayisi)
        yeni_deger = komsu[index] + self.random.uniform(self.komsu_alt_delta, self.komsu_ust_delta)
        komsu[index] = min(self.ust_sinir, max(self.alt_sinir, yeni_deger))
        return komsu

    def kabul_olasiligi(self, mevcut_maliyet, aday_maliyet, sicaklik):
        if aday_maliyet < mevcut_maliyet:
            return 1.0
        fark = aday_maliyet - mevcut_maliyet
        return math.exp(-fark / max(sicaklik, 1e-12))

    def optimize(self, iterasyon_sayisi=1000):
        mevcut_cozum = self.initzalite()
        mevcut_maliyet = self.maliyet_fonksiyonu(mevcut_cozum)

        en_iyi_cozum = mevcut_cozum.copy()
        en_iyi_maliyet = mevcut_maliyet

        sicaklik = self.baslangic_sicakligi
        maliyet_gecmisi = [en_iyi_maliyet]

        for _ in range(iterasyon_sayisi):
            if sicaklik <= self.min_sicaklik:
                break

            aday_cozum = self.komsu_uret(mevcut_cozum)
            aday_maliyet = self.maliyet_fonksiyonu(aday_cozum)

            kabul = self.kabul_olasiligi(mevcut_maliyet, aday_maliyet, sicaklik)
            if self.random.random() < kabul:
                mevcut_cozum = aday_cozum
                mevcut_maliyet = aday_maliyet

            if mevcut_maliyet < en_iyi_maliyet:
                en_iyi_cozum = mevcut_cozum.copy()
                en_iyi_maliyet = mevcut_maliyet

            maliyet_gecmisi.append(en_iyi_maliyet)
            sicaklik *= self.sogutma_katsayisi

        return {
            "en_iyi_cozum": en_iyi_cozum,
            "en_iyi_maliyet": en_iyi_maliyet,
            "maliyet_gecmisi": maliyet_gecmisi,
            "final_sicaklik": sicaklik,
        }




if __name__ == "__main__":
    def amac_fonksiyonu(cozum):
        x1, x2 = cozum
        return x1 ** 2 + 2 * x1 * x2 - x2 ** 3

    optimizer = DogalIsilIslem(islem_sayisi=2, maliyet_fonksiyonu=amac_fonksiyonu, random_seed=42)
    sonuc = optimizer.optimize(iterasyon_sayisi=1000)
    print("En İyi Çözüm:", sonuc["en_iyi_cozum"])
    print("En İyi Maliyet:", sonuc["en_iyi_maliyet"])
    
    


