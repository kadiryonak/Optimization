import math
import random


class YapayIsilIslem:
    """Yapay isil islem (Tavlama Benzetimi / Simulated Annealing).

    Metallerin tavlanmasindan esinlenir: metal once yuksek sicakliga
    isitilir, sonra YAVASCA sogutulursa atomlar dusuk enerjili (kararli)
    bir yapiya yerlesir. Optimizasyonda:
        - sicaklik (T)  -> kotu cozumleri kabul etme olasiligini kontrol eder
        - enerji        -> maliyet (amac) fonksiyonu
        - sogutma       -> T'nin zamanla azaltilmasi

    Metropolis kabul kriteri:
        - Aday cozum daha iyiyse (maliyet dusukse) her zaman kabul edilir.
        - Daha kotuyse  exp(-Δ/T)  olasilikla kabul edilir.
      T buyukken kotu cozumler kolayca kabul edilir (kesfetme / exploration),
      T kuculdukce algoritma giderek daha "acgozlu" olur (somurme / exploitation).

    'dogal_ısıl_islem.py' ile farklari (karsilastirma icin):
        - Sogutma: burada HER iterasyonda surekli geometrik sogutma (T *= alpha),
          digerinde basamakli (her N iterasyonda bir) sogutma vardir.
        - Komsu uretimi: burada Gauss (normal) dagilimli perturbasyon,
          digerinde duzgun (uniform) dagilim kullanilir.
    """

    def __init__(
        self,
        islem_sayisi,
        maliyet_fonksiyonu=None,
        alt_sinir=-10.0,
        ust_sinir=10.0,
        baslangic_sicakligi=400.0,
        min_sicaklik=0.001,
        sogutma_katsayisi=0.99,
        komsu_adim=0.5,
        random_seed=42,
    ):
        self.islem_sayisi = islem_sayisi
        self.alt_sinir = alt_sinir
        self.ust_sinir = ust_sinir
        self.baslangic_sicakligi = baslangic_sicakligi
        self.min_sicaklik = min_sicaklik
        self.sogutma_katsayisi = sogutma_katsayisi
        self.komsu_adim = komsu_adim  # Gauss perturbasyonunun standart sapmasi

        self.maliyet_fonksiyonu = maliyet_fonksiyonu or self.varsayilan_maliyet
        self.random = random.Random(random_seed)

    def varsayilan_maliyet(self, cozum):
        if len(cozum) != 2:
            raise ValueError("Bu varsayilan maliyet fonksiyonu icin islem_sayisi 2 olmalidir.")
        x1, x2 = cozum
        return x1 ** 2 + 2 * x1 * x2 - x2 ** 3

    def random_cozum(self):
        return [self.random.uniform(self.alt_sinir, self.ust_sinir)
                for _ in range(self.islem_sayisi)]

    def komsu_uret(self, cozum):
        """Tek bir degiskeni Gauss gurultusuyle oynatarak komsu cozum uretir."""
        komsu = cozum.copy()
        index = self.random.randrange(self.islem_sayisi)
        yeni_deger = komsu[index] + self.random.gauss(0.0, self.komsu_adim)
        # Sinirlarin disina tasmayi engelle (clamp).
        komsu[index] = min(self.ust_sinir, max(self.alt_sinir, yeni_deger))
        return komsu

    def kabul_olasiligi(self, mevcut_maliyet, aday_maliyet, sicaklik):
        """Metropolis kriteri: daha iyiyse 1.0, degilse exp(-Δ/T)."""
        if aday_maliyet < mevcut_maliyet:
            return 1.0
        fark = aday_maliyet - mevcut_maliyet
        return math.exp(-fark / max(sicaklik, 1e-12))

    def optimize(self, iterasyon_sayisi=10000, raporlama=False, rapor_araligi=100):
        mevcut_cozum = self.random_cozum()
        mevcut_maliyet = self.maliyet_fonksiyonu(mevcut_cozum)

        en_iyi_cozum = mevcut_cozum.copy()
        en_iyi_maliyet = mevcut_maliyet

        sicaklik = self.baslangic_sicakligi
        maliyet_gecmisi = [en_iyi_maliyet]
        kabul_sayisi = 0
        rapor = []

        if raporlama:
            mesaj = f"Baslangic | T={sicaklik:.4f} | mevcut={mevcut_maliyet:.6f} | en_iyi={en_iyi_maliyet:.6f}"
            print(mesaj)
            rapor.append(mesaj)

        for i in range(iterasyon_sayisi):
            if sicaklik <= self.min_sicaklik:
                break

            aday_cozum = self.komsu_uret(mevcut_cozum)
            aday_maliyet = self.maliyet_fonksiyonu(aday_cozum)

            if self.random.random() < self.kabul_olasiligi(mevcut_maliyet, aday_maliyet, sicaklik):
                mevcut_cozum = aday_cozum
                mevcut_maliyet = aday_maliyet
                kabul_sayisi += 1

            if mevcut_maliyet < en_iyi_maliyet:
                en_iyi_cozum = mevcut_cozum.copy()
                en_iyi_maliyet = mevcut_maliyet

            maliyet_gecmisi.append(en_iyi_maliyet)

            if raporlama and ((i + 1) % rapor_araligi == 0 or i == iterasyon_sayisi - 1):
                mesaj = (
                    f"Iterasyon {i + 1:5d} | T={sicaklik:.4f} | mevcut={mevcut_maliyet:.6f} "
                    f"| en_iyi={en_iyi_maliyet:.6f}"
                )
                print(mesaj)
                rapor.append(mesaj)

            # Surekli geometrik sogutma: her iterasyonda sicakligi azalt.
            sicaklik *= self.sogutma_katsayisi

        if raporlama:
            mesaj = (
                f"Bitis    | T={sicaklik:.4f} | en_iyi={en_iyi_maliyet:.6f} "
                f"| kabul_orani={kabul_sayisi / max(1, i + 1):.2%} | cozum={en_iyi_cozum}"
            )
            print(mesaj)
            rapor.append(mesaj)

        return {
            "en_iyi_cozum": en_iyi_cozum,
            "en_iyi_maliyet": en_iyi_maliyet,
            "maliyet_gecmisi": maliyet_gecmisi,
            "final_sicaklik": sicaklik,
            "kabul_sayisi": kabul_sayisi,
            "rapor": rapor,
        }


if __name__ == "__main__":
    def amac_fonksiyonu(cozum):
        x1, x2 = cozum
        return x1 ** 2 + 2 * x1 * x2 - x2 ** 3

    optimizer = YapayIsilIslem(islem_sayisi=2, maliyet_fonksiyonu=amac_fonksiyonu, random_seed=42)
    sonuc = optimizer.optimize(iterasyon_sayisi=1500, raporlama=True, rapor_araligi=100)
    print("En Iyi Cozum:", sonuc["en_iyi_cozum"])
    print("En Iyi Maliyet:", sonuc["en_iyi_maliyet"])
