import numpy as np


class NewtonSearch:
    """Newton (Newton-Raphson) optimizasyon yontemi.

    Newton yontemi, fonksiyonu mevcut nokta etrafinda ikinci dereceden
    (kuadratik) bir Taylor aciliminla yaklasiklar ve bu yaklasimi tek
    adimda minimumlar:

        f(x + d) ~ f(x) + g^T d + (1/2) d^T H d

    Bu kuadratik modelin minimumu  H d = -g  denkleminden bulunur:

        d = -H^(-1) g            (Newton yonu)
        x_(t+1) = x_t + d

    En dik inisten farki, sadece gradyenti (egim) degil, Hessian'i
    (egrilik) de kullanmasidir. Bu sayede kuadratik fonksiyonlarda
    TEK ADIMDA yakinsar; kuadratik olmayan fonksiyonlarda ise minimuma
    yaklastikca cok hizli (karesel) yakinsar.
    """

    def __init__(self, func, grad, hess=None, x0=None, tol=1e-6, max_iter=100):
        self.func = func
        self.grad = grad
        self.hess = hess  # Verilmezse sayisal (sonlu fark) Hessian kullanilir.
        self.x0 = np.array(x0, dtype=float)
        self.tol = tol
        self.max_iter = max_iter
        self.history = []

    def _numerical_hessian(self, x, h=1e-5):
        """Hessian analitik verilmediginde merkezi sonlu farkla hesaplar."""
        n = x.size
        H = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                x_pp = x.copy(); x_pp[i] += h; x_pp[j] += h
                x_pm = x.copy(); x_pm[i] += h; x_pm[j] -= h
                x_mp = x.copy(); x_mp[i] -= h; x_mp[j] += h
                x_mm = x.copy(); x_mm[i] -= h; x_mm[j] -= h
                H[i, j] = (self.func(x_pp) - self.func(x_pm)
                           - self.func(x_mp) + self.func(x_mm)) / (4 * h * h)
        return H

    def solve(self):
        x = self.x0.copy()
        for i in range(self.max_iter):
            grad = self.grad(x)
            # Gradyentin normu toleranstan kucukse duragan noktaya ulasilmistir.
            if np.linalg.norm(grad) < self.tol:
                break

            H = self.hess(x) if self.hess is not None else self._numerical_hessian(x)

            # Newton yonu: H d = -g  =>  d = -H^(-1) g
            # Tersi acikca almak yerine lineer sistem cozmek daha kararlidir.
            try:
                d = np.linalg.solve(H, -grad)
            except np.linalg.LinAlgError:
                # Hessian tekil ise en dik inis yonune geri don.
                d = -grad

            x = x + d
            self.history.append(x.copy())
        return x


# Ornek (Arora, 1989 tarzinda kuadratik problem)
# f(x1, x2) = x1^2 + x2^2 - 2*x1 - 4*x2 + 5
# Minimum: x_opt = (1, 2), f(x_opt) = 0
# Fonksiyon kuadratik oldugundan Newton, baslangic noktasi ne olursa olsun
# TEK ITERASYONDA cozume ulasir.

if __name__ == "__main__":
    # Fonksiyon tanimi
    def f(x):
        return x[0]**2 + x[1]**2 - 2 * x[0] - 4 * x[1] + 5

    # Gradyent: df/dx1 = 2x1 - 2,  df/dx2 = 2x2 - 4
    def grad(x):
        return np.array([2 * x[0] - 2, 2 * x[1] - 4])

    # Hessian: sabit matris [[2, 0], [0, 2]]
    def hess(x):
        return np.array([[2.0, 0.0],
                         [0.0, 2.0]])

    # Minimumdan uzak bir baslangic noktasi
    x0 = [10, -5]

    nw = NewtonSearch(func=f, grad=grad, hess=hess, x0=x0)
    sonuc = nw.solve()

    print(f"Optimum nokta   : x = {sonuc}")
    print(f"Fonksiyon degeri: f(x) = {f(sonuc):.6f}")
    print(f"Iterasyon sayisi: {len(nw.history)}")
