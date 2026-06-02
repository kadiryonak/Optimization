import math
import random


class AntColonyTSP:
    """Karinca Koloni Optimizasyonu (ACO) - Gezgin Satici Problemi (TSP).

    Amac: Tum sehirleri birer kez ziyaret edip baslangica donen EN KISA turu
    bulmak. Cozum bir permutasyon (sehir sirasi) olarak temsil edilir.

    Bu dosyayi ADIM ADIM kuruyoruz. Su an 1. ADIM: problem kurulumu.
      - sehirler        : (x, y) koordinatlari
      - mesafe matrisi  : d[i][j] = i ve j sehirleri arasi Oklit uzakligi
      - sezgisel matris : eta[i][j] = 1 / d[i][j]  (kisa kenar = yuksek cekim)
      - feromon matrisi : tau[i][j]  (baslangicta her kenar esit cazibede)
    """

    def __init__(
        self,
        sehirler,
        alpha=1.0,        # feromonun agirligi
        beta=5.0,         # sezgisel bilginin (1/mesafe) agirligi
        ro=0.5,           # buharlasma orani (rho)
        q=100.0,          # feromon birakma sabiti Q
        baslangic_feromon=1.0,
        random_seed=42,
    ):
        self.sehirler = sehirler
        self.n = len(sehirler)
        if self.n < 2:
            raise ValueError("En az 2 sehir gerekir.")

        self.alpha = alpha
        self.beta = beta
        self.ro = ro
        self.q = q
        self.random = random.Random(random_seed)

        # Mesafe ve sezgisel matrisleri bir kez hesapla (degismez).
        self.mesafe = self._mesafe_matrisi()
        self.eta = self._sezgisel_matris()

        # Feromon matrisi: baslangicta tum kenarlar esit.
        self.tau = [[baslangic_feromon] * self.n for _ in range(self.n)]

    def _mesafe_matrisi(self):
        d = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    xi, yi = self.sehirler[i]
                    xj, yj = self.sehirler[j]
                    d[i][j] = math.hypot(xi - xj, yi - yj)
        return d

    def _sezgisel_matris(self):
        # eta[i][j] = 1 / d[i][j]. Kosegen (i==j) kullanilmaz, 0 birakilir.
        eta = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    eta[i][j] = 1.0 / self.mesafe[i][j]
        return eta

    def tur_uzunlugu(self, tur):
        """Bir turun (sehir sirasinin) toplam uzunlugu; baslangica donus dahil."""
        toplam = 0.0
        for k in range(self.n):
            i = tur[k]
            j = tur[(k + 1) % self.n]  # son sehirden ilk sehre kapan
            toplam += self.mesafe[i][j]
        return toplam


if __name__ == "__main__":
    # Kucuk ornek: 5 sehir (x, y)
    sehirler = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3)]

    aco = AntColonyTSP(sehirler)

    print("Sehir sayisi:", aco.n)
    print("\nMesafe matrisi:")
    for satir in aco.mesafe:
        print("  " + "  ".join(f"{d:5.2f}" for d in satir))

    # Ornek bir tur (sirayla 0->1->2->3->4->0) ne kadar uzun?
    ornek_tur = [0, 1, 2, 3, 4]
    print("\nOrnek tur:", ornek_tur, "uzunluk =", round(aco.tur_uzunlugu(ornek_tur), 3))
