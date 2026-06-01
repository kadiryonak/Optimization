# 1) Türev Tabanlı Yöntemler

Amaç fonksiyonunun **gradyentini** (ve Newton'da **Hessian'ını**) kullanarak
minimuma ilerleyen klasik optimizasyon yöntemleri. Genel iterasyon şeması:

```
x_(t+1) = x_t + alpha * d_t
```

- `d_t` : arama yönü (yöntemler bu yönü farklı seçer)
- `alpha`: adım büyüklüğü (line search / doğrusal arama ile bulunur)

| Dosya | Yön seçimi (`d`) | Notlar |
|-------|------------------|--------|
| `en_dik_inis.py` | `d = -g` (negatif gradyent) | En basit yöntem; zikzak yapabilir |
| `eslenik_gradyent.py` | `d = -g + beta*d_prev` | Fletcher-Reeves; en dik inişe göre daha hızlı |
| `newton_arastirma.py` | `d = -H^(-1) g` | Hessian'ı kullanır; kuadratikte tek adımda yakınsar |

Tüm dosyalar `numpy` gerektirir ve `__main__` bloğunda Arora (1989) tarzı
örnek problemlerle çalıştırılabilir.
