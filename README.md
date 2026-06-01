# Optimization

Optimizasyon algoritmalarını öğrenmek amacıyla, **Prof. Dr. Derviş Karaboğa'nın
"Yapay Zekâ Optimizasyon Algoritmaları"** kitabı temel alınarak yazdığım
Python uygulamaları. Amaç, algoritmaları kod üzerinden adım adım anlamak.

## İçerik

### 1) Türev Tabanlı Yöntemler — `1-) turev_tabanli/`
Gradyent (ve gerekiyorsa Hessian) bilgisini kullanan klasik yöntemler.

| Dosya | Algoritma |
|-------|-----------|
| `en_dik_inis.py` | En Dik İniş (Steepest Descent) |
| `eslenik_gradyent.py` | Eşlenik Gradyent (Fletcher-Reeves) |
| `newton_arastirma.py` | Newton (Newton-Raphson) yöntemi |

### 2) Sezgisel Algoritmalar — `2-) sezgisel_algoritmalar/`
Türev gerektirmeyen, rastgeleliğe dayalı sezgisel (metasezgisel) yöntemler.

| Dosya | Algoritma |
|-------|-----------|
| `dogal_ısıl_islem.py` | Tavlama Benzetimi — basamaklı soğutma |
| `yapay_ısıl_islem.py` | Tavlama Benzetimi — sürekli geometrik soğutma |
| `tabu.py` | Tabu Arama (aspirasyon kriterli) |
| `genetic_algorithm.py` | Genetik Algoritma (BBOB f15 Rastrigin) |

## Çalıştırma

Her dosya kendi başına çalıştırılabilir bir örnek içerir:

```bash
python "1-) turev_tabanli/en_dik_inis.py"
python "2-) sezgisel_algoritmalar/tabu.py"
```

Gereksinimler: `numpy` (türev tabanlı yöntemler için).
`genetic_algorithm.py` opsiyonel olarak `cocoex` (gerçek BBOB) kullanır; kurulu
değilse kanonik Rastrigin'e otomatik geri döner.

```bash
pip install numpy
pip install cocoex   # opsiyonel
```

> Not: Kaynak kitabın PDF'i telif nedeniyle depoya dahil edilmez (`.gitignore`).
