# 2) Sezgisel Algoritmalar

Türev bilgisi gerektirmeyen, **rastgeleliğe** ve **arama stratejilerine** dayalı
metasezgisel yöntemler. Çok tepeli (multimodal) ve türevi alınamayan
problemlerde, yerel minimuma takılmadan global minimumu aramaya çalışırlar.

| Dosya | Algoritma | Temel fikir |
|-------|-----------|-------------|
| `dogal_ısıl_islem.py` | Tavlama Benzetimi | Kötü çözümleri sıcaklığa bağlı olasılıkla kabul; **basamaklı** soğutma |
| `yapay_ısıl_islem.py` | Tavlama Benzetimi | Aynı Metropolis kriteri; **sürekli geometrik** soğutma + Gauss komşuluk |
| `tabu.py` | Tabu Arama | Son hamleleri "tabu listesi"nde tutarak döngüye girmeyi önler |
| `genetic_algorithm.py` | Genetik Algoritma | Seçilim + çaprazlama + mutasyon ile popülasyonu evrimleştirir |

## Ortak deney problemi

`dogal_ısıl_islem.py`, `yapay_ısıl_islem.py` ve `tabu.py` aynı amaç
fonksiyonunu kullanır; böylece üç yöntem aynı problem üzerinde karşılaştırılabilir:

```
f(x1, x2) = x1^2 + 2*x1*x2 - x2^3        (sınırlar: [-10, 10])
```

> Not: Bu fonksiyon alttan sınırsızdır (x2 → +∞ iken −x2³ → −∞), bu yüzden
> minimum, tanım kümesinin sınırında oluşur. Algoritmaların davranışını
> gözlemlemek için uygundur.

`genetic_algorithm.py` ise literatür kıyaslaması olarak **BBOB f15 (Rastrigin)**
problemini çözer (`cocoex` kuruluysa gerçeğini, değilse kanonik halini kullanır).
