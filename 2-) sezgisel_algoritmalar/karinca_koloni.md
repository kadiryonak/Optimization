# Karınca Koloni Optimizasyonu (ACO) — Ders Notları

> Kaynak: El yazısı ders notları (Aybüke Arpacı, 2018) + Prof. Dr. Derviş Karaboğa,
> *Yapay Zekâ Optimizasyon Algoritmaları* (nümerik/TACO detayları için **Sf. 121**).
> Bu doküman `1.png–4.png` notlarındaki kritik yerleri matematik + kod ile açıklar.

İçindekiler:
1. [Sürü zekâsı temelli algoritmalar](#1-sürü-zekâsı-temelli-algoritmalar)
2. [Sürü zekâsının (swarm) şartları — KRİTİK](#2-sürü-zekâsının-swarm-şartları--kritik)
3. [Gerçek karınca vs. yapay karınca](#3-gerçek-karınca-vs-yapay-karınca)
4. [ACO'nun temel operatörleri](#4-aconun-temel-operatörleri)
5. [ACO'nun temel adımları](#5-aconun-temel-adımları)
6. [Gezgin Satıcı Problemi (TSP) — matematik + kod](#6-gezgin-satıcı-problemi-tsp--matematik--kod)
7. [Nümerik problemler için ACO (CACO / GACO / TACO)](#7-nümerik-problemler-için-aco-caco--gaco--taco)
8. [Kritik noktalar — özet](#8-kritik-noktalar--özet)

---

## 1. Sürü Zekâsı Temelli Algoritmalar

- **Sosyal hayvanlar:** Doğada koloni hâlinde yaşayan, aralarında belirli bir **iş paylaşımı**
  olan ve karşılaştıkları problemleri **yardımlaşarak birlikte çözen** hayvanlardır.
- **Swarm (zeki sürü):** Birbirine benzer, problem çözmede **sınırlı yeteneklere** sahip, belirli
  prensipleri yerine getiren, zeki davranışlar sergileyen topluluklardır. Tek birey "aptal"dır;
  zekâ **topluluğun davranışından ortaya çıkar** (emergent / ortaya çıkan zekâ).
- Zeki sürüler yaşamlarının **her aşamasında** zekilik gösterir (yuva yapımı, yiyecek temini, …).
- **ACO'da** karıncaların **sadece yiyecek toplama** aşamasındaki zeki davranışı ele alınır.

### Evrimsel temelli vs. Sürü zekâsı temelli — temel fark

| | Evrimsel algoritmalar (GA) | Sürü zekâsı temelli (ACO, ABC, PSO…) |
|---|---|---|
| Dayanak | Doğal **seleksiyon + çaprazlama** | **Topluluğun davranışından** ortaya çıkan zekâ |
| Kontrol | — | **Merkezî emir YOK**, sadece **bölgesel (yerel) etkileşim** |

> **Kritik:** Sürü zekâsında merkezî bir yönetici yoktur. Her birey yalnızca yerel bilgiyle
> (komşuluk, feromon) karar verir; küresel düzen bu yerel kararlardan kendiliğinden doğar.

---

## 2. Sürü Zekâsının (Swarm) Şartları — KRİTİK

Bir algoritmanın "sürü zekâsı" sayılabilmesi için notlardaki **iki temel şart**:

### a) İş bölümü olmalı
Bireylerin **yapacakları işler belli** olmalı (görevler topluluk içinde dağıtılmış).

### b) Kendi kendine organize olabilme (self-organization)
Merkezden emir almak yerine, **topluluk olarak kendi davranışlarını** üretebilmeli.
Kendi kendine organizasyonun **4 bileşeni**:

| # | Bileşen | Hangi mekanizma |
|---|---------|-----------------|
| i | **Pozitif geri besleme** | **Seleksiyon** |
| ii | **Negatif geri besleme** | **Seleksiyon** |
| iii | **Rastlantısal (random) davranış** | **Değişim (çeşitlilik)** |
| iv | **Çoklu etkileşim** | **Yardımlaşma** |

Karınca bağlamında karşılıkları:
- **Pozitif geri besleme:** İyi bir davranışı yapan bireyin örnek alınması; iyi yöne giden
  karınca sayısının artması → o yola daha çok feromon → daha çok karınca (kendini güçlendiren döngü).
- **Negatif geri besleme:** Faydasız yolun terk edilmesi; feromonun **buharlaşması** sayesinde
  kötü yollar zamanla unutulur (aksi hâlde sistem ilk bulduğu yola saplanır).
- **Rastlantısallık:** Karıncalar her zaman en iyi yolu seçmez; olasılıkla bazen kötü yolu da
  dener → **keşif (exploration)**, yerel optimuma takılmayı önler.
- **Çoklu etkileşim:** Karıncalar feromon üzerinden **dolaylı haberleşir** (stigmerji).

> **Karıncanın amacı:** Yuva ile yiyecek arasında **harcanan enerjiyi minimize**,
> **yuvaya taşınan yiyecek miktarını maksimize** etmek → bunun için **en kısa yolu** bulmak gerekir.
> Karıncaların **en kısa yolu keşfetme kabiliyeti** vardır.

---

## 3. Gerçek Karınca vs. Yapay Karınca

Karıncalar gözleriyle iyi göremez; gittikleri yere **koku (feromon)** bırakıp **kokuyu referans
alarak** yön bulurlar. ACO bu **feromon tabanlı** haberleşmeyi taklit eder.

| Gerçek karınca | Yapay karınca (ACO) |
|---|---|
| **Hafızasız** | **Hafızalı** (gittiği şehirleri tutar → tabu listesi) |
| **Sürekli (continuous) zamanda** çalışır | **Ayrık (discrete) zamanda** çalışır |
| Her karıncanın bıraktığı koku **miktarı eşit** | **Farklı miktarlarda** koku bırakabilir (yol kalitesine göre) |
| Yolu **geçerken** koku bırakır | Yolu **geçtikten sonra** (tur bitince) koku bırakır |
| Tüm muhtemel yollar = muhtemel çözümler | Her karınca = problemin **bir alternatif çözümü** |

> **Kritik fark:** Yapay karınca **hafızalı**dır; bir şehre tekrar uğramamak için ziyaret
> ettiklerini **tabu listesinde** tutar. Ayrıca feromonu **tur tamamlandıktan sonra** bırakır
> (gerçek karınca yürürken bırakır).

---

## 4. ACO'nun Temel Operatörleri

1. **Feromon (τ):** Kenarlarda biriken "öğrenilmiş cazibe". Koloninin **ortak hafızası**.
2. **Sezgisel bilgi (η):** Probleme özgü açgözlü ipucu. TSP'de $\eta_{ij}=1/d_{ij}$ (kısa kenar → yüksek çekim).
3. **Olasılıksal seçim kuralı (P):** Feromon ve sezgiseli birleştirip bir sonraki adımı **rastgele
   ama eğilimli** seçer.
4. **Buharlaşma (evaporation):** Feromonu zamanla azaltır → negatif geri besleme, takılmayı önler.
5. **Koku bırakma (deposit):** İyi (kısa) turlar kenarlarına daha çok feromon ekler → pozitif geri besleme.

---

## 5. ACO'nun Temel Adımları

```
Adım 1: Başlangıç yapay yolları üret ve kontrol parametrelerini ata (α, β, ρ, Q, karınca sayısı).
Adım 2: Yol uzunluklarından her yapay karıncanın bırakacağı koku miktarını hesapla.
        (Yol uzunluğu arttıkça bırakılan koku miktarı DÜŞER → Δτ ∝ 1/L)
Adım 3: Yollardaki (kenarlardaki) koku miktarını güncelle (buharlaşma + bırakma).
Adım 4: En kısa yolu hafızada tut ve yeni yapay yollar üret.
Adım 5: Durdurma kriteri sağlanmıyorsa Adım 2'ye git.
```

---

## 6. Gezgin Satıcı Problemi (TSP) — Matematik + Kod

**Tanım:** $n$ şehir verildiğinde, her şehri **bir kez** ziyaret edip başlangıca dönen
**minimum uzunlukta kapalı tur**u bulma problemi. ACO'nun makalede **ilk tanıtıldığı** problemdir.
Genelde $m$ (örn. 100) karınca kullanılır; her karınca bir tur kurar, $m$ karınca = $m$ aday yol.
**Turlar tamamlandıktan sonra** koku bırakma yapılır.

### 6.1 Mesafe (iki şehir arası, Öklit)

$$ d_{ij} = \left[ (x_i - x_j)^2 + (y_i - y_j)^2 \right]^{1/2} $$

```python
import math
d_ij = math.hypot(x_i - x_j, y_i - y_j)   # = sqrt((xi-xj)^2 + (yi-yj)^2)
```

### 6.2 Koloni büyüklüğü

$m$ = kolonideki toplam karınca sayısı. $t$ anında $i$ şehrinde bulunan karınca sayısı $b_i(t)$ ise:

$$ m = \sum_{i=1}^{n} b_i(t) $$

### 6.3 Sezgisel (görünürlük) bilgisi

$$ \eta_{ij} = \frac{1}{d_{ij}} \qquad\text{(kısa kenar} \Rightarrow \text{yüksek } \eta) $$

### 6.4 Olasılıksal geçiş kuralı (KRİTİK formül)

$k$-ıncı karıncanın $i$ şehrinden $j$ şehrine geçme olasılığı:

$$
P_{ij}^{k}(t) =
\begin{cases}
\dfrac{[\tau_{ij}(t)]^{\alpha}\,[\eta_{ij}]^{\beta}}
       {\displaystyle\sum_{l \,\in\, \text{izin verilenler}} [\tau_{il}(t)]^{\alpha}\,[\eta_{il}]^{\beta}}
& \text{eğer } j \notin \text{tabu}_k \quad(\text{daha önce uğranmadıysa})\\[2.2em]
0 & \text{aksi hâlde (}j\text{ tabu listesinde)}
\end{cases}
$$

- $\alpha$: **feromonun** ağırlığı (geçmiş deneyim). $\alpha=0$ → saf açgözlü (sadece mesafe).
- $\beta$: **sezgiselin** ağırlığı (kısa kenar isteği). $\beta=0$ → sadece feromon (kör taklit).
- **tabu listesi** = karıncanın bu turda ziyaret ettiği şehirler (hafıza → tekrar uğranmaz).

```python
def gecis_olasiliklari(self, mevcut, ziyaret_edilmemis):
    pay = {}
    for j in ziyaret_edilmemis:                       # sadece tabu OLMAYANLAR
        pay[j] = (self.tau[mevcut][j] ** self.alpha) * (self.eta[mevcut][j] ** self.beta)
    toplam = sum(pay.values())                        # payda = normalizasyon
    return {j: p / toplam for j, p in pay.items()}    # P_ij olasılıkları (toplamı 1)

def sonraki_sehri_sec(self, mevcut, ziyaret_edilmemis):
    olasiliklar = self.gecis_olasiliklari(mevcut, ziyaret_edilmemis)
    # Rulet tekerleği: olasılıkla seç (her zaman en iyiyi DEĞİL → keşif/rastlantısallık)
    r = self.random.random()
    kumulatif = 0.0
    for j, p in olasiliklar.items():
        kumulatif += p
        if r <= kumulatif:
            return j
    return next(iter(olasiliklar))                    # sayısal güvenlik
```

### 6.5 Feromon güncelleme (KRİTİK formül)

Notlardaki konvansiyon — $\rho$ **korunan** feromonun katsayısı (1'den küçük pozitif):

$$ \tau_{ij}(t+1) = \rho \cdot \tau_{ij}(t) + \Delta\tau_{ij}(t,\,t+1) $$

- **Buharlaşma katsayısı $\rho < 1$:** Feromonun sınırsız büyümesini önler (negatif geri besleme).
- Bırakılan toplam koku, tüm karıncaların katkısının toplamıdır:

$$ \Delta\tau_{ij}(t,\,t+1) = \sum_{k=1}^{m} \Delta\tau_{ij}^{k}(t,\,t+1) $$

- $\Delta\tau_{ij}^{k}$ = $k$-ıncı karıncanın $(i,j)$ kenarına bıraktığı koku. Klasik kural
  (yol uzadıkça koku düşer):

$$
\Delta\tau_{ij}^{k} =
\begin{cases}
\dfrac{Q}{L_k} & \text{eğer } k\text{ karıncası } (i,j) \text{ kenarını kullandıysa}\\
0 & \text{aksi hâlde}
\end{cases}
$$

> ⚠️ **İki farklı konvansiyon — karıştırma!**
> - **Notlar (Dorigo orijinali):** $\tau \leftarrow \rho\,\tau + \Delta\tau$ → burada $\rho$ = **kalıcılık**, buharlaşma = $1-\rho$.
> - **Bazı kitaplar:** $\tau \leftarrow (1-\rho)\,\tau + \Delta\tau$ → burada $\rho$ = doğrudan **buharlaşma oranı**.
>
> Yan dosyadaki `karinca_koloni_tsp.py` ikinci konvansiyonu (`(1-ρ)·τ`) kullanır.
> İkisi de doğrudur; **kodda hangisini kullandığını bilerek** parametre seç.

```python
def feromon_guncelle(self, turlar, uzunluklar):
    # 1) Buharlaşma (notlar konvansiyonu: korunan kısım ρ·τ)
    for i in range(self.n):
        for j in range(self.n):
            self.tau[i][j] *= self.ro
    # 2) Bırakma: her karınca kendi turuna Q/L kadar koku ekler (kısa tur → çok koku)
    for tur, L in zip(turlar, uzunluklar):
        katki = self.q / L
        for k in range(self.n):
            i, j = tur[k], tur[(k + 1) % self.n]
            self.tau[i][j] += katki
            self.tau[j][i] += katki        # TSP simetrik → ters kenar da güncellenir
```

---

## 7. Nümerik Problemler için ACO (CACO / GACO / TACO)

> Literatürdeki ACO uygulamalarının çoğu **ayrık (kombinatoryal)** problemler içindir; **nümerik
> (sürekli)** optimizasyon için az çalışma vardır. Notlara göre en iyileri **Hiyerarşi (Bilchev &
> Parmee)** çalışmasıdır ve **üç** algoritma tanımlar:

| Algoritma | Açılım | Temsil / Fikir |
|---|---|---|
| **CACO** | Sürekli problemler için ACO | **2 aşama**: küresel (global) + bölgesel (yerel) araştırma |
| **GACO** | Izgaralı (grid) ACO | Arama uzayı **ızgaralara** bölünür; karıncalar iyi ızgara noktalarını araştırır |
| **TACO** | **Tur eden** ACO | Çözümler **binary bitlerle** temsil; karıncalar her bitin 0/1 değerini araştırır |

**TACO neden öne çıkıyor (notlardan):**
- İlk iki algoritmadan **daha iyi**.
- **En az kontrol parametresi** olan algoritma.
- **Daha esnek ve daha basit.**

### 7.1 TACO'nun çalışma mantığı (KRİTİK)

Çözüm $x=(x_1, x_2, \dots)$ **binary bit dizisiyle** kodlanır. Karınca, soldan sağa bir **graf**
üzerinde ilerler; **her bit pozisyonunda 2 yön** vardır: **0** veya **1**. Hangi yöne gideceğini o
kenarlardaki **feromona göre olasılıkla** seçer. Bütün bitler seçilince **bir yol = bir çözüm**
oluşur.

```
        bit1   bit2   bit3      ...
       ┌─0─┐  ┌─0─┐  ┌─0─┐
yuva ──┤   ├──┤   ├──┤   ├── ... ── çözüm (geri üretilen yol)
       └─1─┘  └─1─┘  └─1─┘
   (her düğümde 2 seçenek: feromonu yüksek olan yön daha olası)
```

- **Her karınca farklı yollar** bulur (farklı bit dizileri).
- Bulunan yol (bit dizisi) **amaç fonksiyonuna** $f(x_1, x_2)$ konulur, sonuca göre **koku miktarı**
  hesaplanır (iyi çözüm → çok koku).
- **Her aşamada 2 yön** vardır (0/1).
- Karıncanın **geri gitmemesi** için yine **hafıza** kullanılır.

### 7.2 TACO matematiği

Her $i$ bit pozisyonu için iki feromon değeri tutulur: $\tau_{i,0}$ ve $\tau_{i,1}$.
$i$ bitinin **1** seçilme olasılığı (sezgisel yok → en az parametre):

$$
P(b_i = 1) = \frac{\tau_{i,1}^{\,\alpha}}{\tau_{i,0}^{\,\alpha} + \tau_{i,1}^{\,\alpha}},
\qquad P(b_i = 0) = 1 - P(b_i = 1)
$$

**Binary → reel çözüm (kod çözme).** $D$ değişken, her biri $L$ bit ise, bir değişkenin biti
$[a,b]$ aralığına ölçeklenir:

$$
x_d = a + \frac{\text{int}_2(b_{(d)})}{2^{L}-1}\,(b - a)
$$

**Koku güncelleme (minimizasyon).** Yol kalitesi arttıkça (maliyet $f$ düştükçe) koku artar:

$$
\tau_{i,v}(t+1) = \rho\,\tau_{i,v}(t) + \sum_{k:\, b_i^{k}=v} \frac{Q}{f(x^k)}
$$

(Burada $v\in\{0,1\}$; minimumda $f$ negatif/0 olabiliyorsa $Q/(1+f-f_{min})$ gibi pozitif bir
ölçek kullanılır.)

### 7.3 TACO temel adımları (A1–A6)

```
A1: Parametrelere ve hatların (kenarların) feromon miktarına başlangıç değerlerini ata,
    sayacı sıfırla.
A2: Aşağıdaki adımları durdurma kriteri sağlanıncaya kadar TEKRARLA:
A3:   Tüm karıncalar için feromon miktarına bağlı olarak yollar (bit dizileri) üret.
A4:   Yolları çöz (binary→reel) ve uzunluklarını/maliyetlerini hesapla: f(x).
A5:   Yolların kalitesine göre kenarlardaki feromon miktarını değiştir (buharlaşma + bırakma).
A6:   Şu ana kadar bulunan en iyi (en kısa) yolu hafızada tut.
```

### 7.4 TACO çekirdek kod iskeleti

```python
def bit_sec(self, i):
    """i. bit pozisyonu için 0/1 değerini feromona göre olasılıkla seç."""
    t0 = self.tau[i][0] ** self.alpha
    t1 = self.tau[i][1] ** self.alpha
    p1 = t1 / (t0 + t1)                 # P(b_i = 1)
    return 1 if self.random.random() < p1 else 0

def bir_karinca_yol_kur(self):
    return [self.bit_sec(i) for i in range(self.gen_uzunlugu)]   # bir bit dizisi = bir çözüm

def coz(self, bitler, a=-5.0, b=5.0):
    """Binary diziyi D boyutlu reel vektöre çevir (decode)."""
    L = len(bitler) // self.boyut
    x = []
    for d in range(self.boyut):
        parca = bitler[d*L:(d+1)*L]
        tam = int("".join(map(str, parca)), 2)
        x.append(a + (tam / (2**L - 1)) * (b - a))
    return x

def feromon_guncelle(self, yollar, maliyetler):
    for i in range(self.gen_uzunlugu):          # buharlaşma
        self.tau[i][0] *= self.ro
        self.tau[i][1] *= self.ro
    for bitler, f in zip(yollar, maliyetler):   # bırakma (iyi çözüm → çok koku)
        katki = self.q / (1.0 + max(0.0, f))    # minimizasyon için pozitif ölçek
        for i, v in enumerate(bitler):
            self.tau[i][v] += katki
```

> **Not:** Formüllerin tam detayı için kitap **Sf. 121**. Buradaki ölçekleme ($Q/(1+f)$) notlardaki
> "yol uzunluğu arttıkça koku azalır" ilkesinin minimizasyona uyarlanmış hâlidir.

---

## 8. Kritik Noktalar — Özet

1. **Sürü zekâsının iki şartı:** (a) **iş bölümü**, (b) **kendi kendine organizasyon**
   (pozitif/negatif geri besleme = seleksiyon, rastlantısallık = değişim, çoklu etkileşim = yardımlaşma).
2. **Merkezî emir yok**, sadece **yerel etkileşim**; zekâ topluluktan **ortaya çıkar**.
3. **Pozitif geri besleme** (feromon birikimi) ⇄ **Negatif geri besleme** (buharlaşma) dengesi =
   **sömürü (exploitation) ⇄ keşif (exploration)** dengesi.
4. **Geçiş olasılığı** $P_{ij}\propto \tau^{\alpha}\,\eta^{\beta}$; $\alpha$ feromonu, $\beta$
   sezgiseli ağırlıklandırır; **tabu listesi** tekrar ziyareti engeller.
5. **Feromon güncelleme** iki adımdır: **buharlaşma** ($\rho$) + **bırakma** ($Q/L$). $\rho<1$ şart.
   **İki konvansiyon** ($\rho\tau$ vs. $(1-\rho)\tau$) — kodla notu karıştırma.
6. **Yapay karınca: hafızalı, ayrık zaman, kaliteye göre farklı koku, turu bitince koku bırakır.**
7. **Nümerik = TACO:** çözümü **binary bit** olarak kodla, her biti feromona göre olasılıkla seç,
   decode et, $f(x)$ ile koku hesapla. **En az parametreli, en basit** nümerik ACO.
8. **TSP** kombinatoryal (kenar feromonu), **TACO** nümerik (bit feromonu) — **iki farklı temsil**.
