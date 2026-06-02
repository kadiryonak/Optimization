import math
import random


class YapayAriKoloni:
    """Yapay Ari Koloni (Artificial Bee Colony - ABC) algoritmasi.

    Karaboga (2005) tarafindan, bal arilarinin yiyecek arama davranisindan
    esinlenerek gelistirilmis bir suru zekasi (swarm intelligence) optimizasyon
    algoritmasidir. Surudeki ariler is bolumu yapar:

        - Gorevli ari (employed bee): Belli bir yiyecek kaynagina (cozume)
          baglidir, o kaynagin komsulugunu somurur (exploitation).
        - Gozcu ari (onlooker bee): Kovanda bekler; gorevli arilerin getirdigi
          bilgiye (nektar miktari ~ uygunluk) gore bir kaynagi OLASILIKLA secer.
          Iyi kaynaklar daha cok gozcu ceker -> pozitif geri besleme.
        - Kasif ari (scout bee): Tukenen (gelistirilemeyen) kaynagi birakip
          arama uzayinda RASTGELE yeni bir kaynak bulur (exploration).

    Kaynak <-> cozum esleniigi:
        - Bir yiyecek kaynaginin KONUMU  = optimizasyon problemindeki bir cozum.
        - Kaynagin nektar MIKTARI        = o cozumun uygunlugu (fitness).
        - Kaynak sayisi (SN)             = gorevli ari sayisi = gozcu ari sayisi
                                         = koloni / 2.

    Kesif (exploration) - Somuru (exploitation) dengesi:
        - Gorevli + gozcu fazlari mevcut iyi kaynaklarin etrafini arar -> SOMURU.
        - Kasif fazi tukenen kaynagi atip yeniden rastgele baslatir -> KESIF.
      'limit' parametresi bu dengeyi ayarlar: KUCUK limit -> kaynaklar cabuk
      terk edilir, kesif artar; BUYUK limit -> kaynaklar uzun somurulur,
      somuru artar.

    Kullanilan esitlikler (Karaboga, Bolum 9):
        (9.1) Baslangic kaynagi (ve kasif):
              x_ij = x_j^min + rand(0,1) * (x_j^max - x_j^min)
        (9.2) Komsu (aday) cozum:
              v_ij = x_ij + phi_ij * (x_ij - x_kj),   phi_ij in [-1, 1],  k != i
              (cozumun yalnizca TEK bir j boyutu degisir)
        (9.3) Sinir kontrolu: v_ij uretildigi araligin disina tasarsa kirpilir.
        (9.4) Uygunluk (fitness):
              fit_i = 1 / (1 + f_i)      eger f_i >= 0
              fit_i = 1 + |f_i|          eger f_i <  0
        (9.5) Gozcu secim olasiligi:
              p_i = fit_i / sum_j(fit_j)

    ABC en aza indirme (minimizasyon) icin yazilmistir: amac fonksiyonunun
    degeri (f) ne kadar KUCUKse uygunluk (fit) o kadar BUYUKtur.
    """

    def __init__(
        self,
        amac_fonksiyonu,
        alt_sinir,
        ust_sinir,
        boyut,
        koloni_buyuklugu=40,
        limit=None,
        max_cevrim=1000,
        random_seed=42,
    ):
        """
        amac_fonksiyonu : minimize edilecek f(x); x bir liste (uzunluk = boyut).
        alt_sinir       : skaler ya da boyut uzunlugunda liste (x_j^min).
        ust_sinir       : skaler ya da boyut uzunlugunda liste (x_j^max).
        boyut           : problem boyutu (D).
        koloni_buyuklugu: toplam ari sayisi; SN = koloni / 2 kaynak verir.
        limit           : bir kaynak kac basarisiz denemeden sonra terk edilir.
                          Verilmezse SN * D olarak alinir (yaygin oneri).
        max_cevrim      : toplam cevrim (iterasyon) sayisi.
        """
        self.amac = amac_fonksiyonu
        self.D = boyut
        # Sinirlari her boyut icin listeye genislet (skaler de kabul edilir).
        self.alt = alt_sinir if isinstance(alt_sinir, (list, tuple)) else [alt_sinir] * boyut
        self.ust = ust_sinir if isinstance(ust_sinir, (list, tuple)) else [ust_sinir] * boyut

        self.SN = koloni_buyuklugu // 2  # kaynak = gorevli = gozcu sayisi
        self.limit = limit if limit is not None else self.SN * self.D
        self.max_cevrim = max_cevrim
        self.random = random.Random(random_seed)

        self.en_iyi_cozum = None
        self.en_iyi_maliyet = float("inf")

    # ----------------------------------------------------------------- #
    #  Yardimci hesaplar
    # ----------------------------------------------------------------- #
    def fitness(self, f_degeri):
        """Esitlik 9.4: amac degerini (minimizasyon) uygunluga cevirir."""
        if f_degeri >= 0:
            return 1.0 / (1.0 + f_degeri)
        return 1.0 + abs(f_degeri)

    def rastgele_kaynak(self):
        """Esitlik 9.1: arama uzayinda rastgele bir yiyecek kaynagi uretir."""
        return [self.alt[j] + self.random.random() * (self.ust[j] - self.alt[j])
                for j in range(self.D)]

    def komsu_uret(self, i):
        """Esitlik 9.2 + 9.3: i. kaynaga komsu bir aday cozum (v) uretir.

        Rastgele baska bir k kaynagi (k != i) ve rastgele tek bir j boyutu
        secilir; phi in [-1, 1] ile o boyutta perturbasyon yapilir, sonra
        sinirlara kirpilir.
        """
        v = self.kaynak[i][:]
        j = self.random.randrange(self.D)
        k = self.random.randrange(self.SN)
        while k == i:
            k = self.random.randrange(self.SN)
        phi = self.random.uniform(-1.0, 1.0)
        v[j] = self.kaynak[i][j] + phi * (self.kaynak[i][j] - self.kaynak[k][j])
        # Esitlik 9.3: sinir disina tasmayi engelle (clamp).
        v[j] = min(self.ust[j], max(self.alt[j], v[j]))
        return v

    def acgozlu_secim(self, i, v):
        """Aday v ile mevcut kaynak i arasinda acgozlu (greedy) secim.

        v daha iyiyse (uygunlugu yuksekse) kaynagi gunceller ve basarisizlik
        sayacini sifirlar; degilse sayaci bir artirir (kaynak yaslanir).
        """
        f_v = self.amac(v)
        fit_v = self.fitness(f_v)
        if fit_v > self.fit[i]:
            self.kaynak[i] = v
            self.f[i] = f_v
            self.fit[i] = fit_v
            self.basarisizlik[i] = 0
        else:
            self.basarisizlik[i] += 1

    # ----------------------------------------------------------------- #
    #  Fazlar
    # ----------------------------------------------------------------- #
    def baslat(self):
        """Tum kaynaklari rastgele uret, uygunluklari hesapla (Adim 1)."""
        self.kaynak = [self.rastgele_kaynak() for _ in range(self.SN)]
        self.f = [self.amac(x) for x in self.kaynak]
        self.fit = [self.fitness(v) for v in self.f]
        self.basarisizlik = [0] * self.SN
        self.guncelle_en_iyi()

    def gorevli_ari_fazi(self):
        """Her gorevli ari kendi kaynaginin komsulugunu somurur."""
        for i in range(self.SN):
            self.acgozlu_secim(i, self.komsu_uret(i))

    def olasiliklar(self):
        """Esitlik 9.5: her kaynagin gozcu tarafindan secilme olasiligi."""
        toplam = sum(self.fit)
        if toplam == 0:
            return [1.0 / self.SN] * self.SN
        return [v / toplam for v in self.fit]

    def gozcu_ari_fazi(self):
        """Gozculer, olasiliga (rulet tekeri) gore kaynak secip somurur.

        Toplam SN gozcu yerlestirilene kadar kaynaklar uzerinde donulur;
        bir kaynak olasiligi kadar sansla bir gozcu ceker.
        """
        p = self.olasiliklar()
        i = 0
        yerlesen = 0
        while yerlesen < self.SN:
            if self.random.random() < p[i]:
                self.acgozlu_secim(i, self.komsu_uret(i))
                yerlesen += 1
            i = (i + 1) % self.SN

    def kasif_ari_fazi(self):
        """Basarisizlik sayaci 'limit'i asan kaynak terk edilir (Esitlik 9.1).

        Bir cevrimde en fazla tek kaynak (en cok yaslanmis olan) yeniden
        baslatilir; bu klasik ABC davranisidir.
        """
        i = max(range(self.SN), key=lambda k: self.basarisizlik[k])
        if self.basarisizlik[i] > self.limit:
            self.kaynak[i] = self.rastgele_kaynak()
            self.f[i] = self.amac(self.kaynak[i])
            self.fit[i] = self.fitness(self.f[i])
            self.basarisizlik[i] = 0

    def guncelle_en_iyi(self):
        """Su ana kadar bulunan en iyi cozumu (hafiza) sakla."""
        for i in range(self.SN):
            if self.f[i] < self.en_iyi_maliyet:
                self.en_iyi_maliyet = self.f[i]
                self.en_iyi_cozum = self.kaynak[i][:]

    # ----------------------------------------------------------------- #
    #  Ana dongu
    # ----------------------------------------------------------------- #
    def optimize(self, raporlama=False, rapor_araligi=100):
        self.baslat()
        maliyet_gecmisi = [self.en_iyi_maliyet]

        for cevrim in range(self.max_cevrim):
            self.gorevli_ari_fazi()   # somuru
            self.gozcu_ari_fazi()     # olasilikli somuru
            self.kasif_ari_fazi()     # kesif
            self.guncelle_en_iyi()    # hafiza
            maliyet_gecmisi.append(self.en_iyi_maliyet)

            if raporlama and ((cevrim + 1) % rapor_araligi == 0 or cevrim == self.max_cevrim - 1):
                print(f"Cevrim {cevrim + 1:5d} | en_iyi_maliyet = {self.en_iyi_maliyet:.6e}")

        return {
            "en_iyi_cozum": self.en_iyi_cozum,
            "en_iyi_maliyet": self.en_iyi_maliyet,
            "maliyet_gecmisi": maliyet_gecmisi,
        }


if __name__ == "__main__":
    D = 5

    # Sphere: kuresel minimumu 0 olan, tek tepeli (unimodal) test fonksiyonu.
    def sphere(x):
        return sum(xi * xi for xi in x)

    # Rastrigin: cok sayida yerel minimumu olan (multimodal) zor test fonksiyonu.
    def rastrigin(x):
        return 10 * len(x) + sum(xi * xi - 10 * math.cos(2 * math.pi * xi) for xi in x)

    for ad, fonksiyon in [("Sphere", sphere), ("Rastrigin", rastrigin)]:
        abc = YapayAriKoloni(
            amac_fonksiyonu=fonksiyon,
            alt_sinir=-5.12,
            ust_sinir=5.12,
            boyut=D,
            koloni_buyuklugu=40,
            max_cevrim=1500,
            random_seed=42,
        )
        sonuc = abc.optimize(raporlama=False)
        print(f"{ad:10s} -> en iyi f = {sonuc['en_iyi_maliyet']:.6e}")
