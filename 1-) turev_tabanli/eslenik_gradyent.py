import numpy as np

class ConjugateGradient:
    def __init__(self, func, grad, x0, tol=1e-6, max_iter=1000):
        self.func = func
        self.grad = grad
        self.x0 = np.array(x0, dtype=float)
        self.tol = tol
        self.max_iter = max_iter
        self.history = []

    def _line_search(self, x, d):
        """Verilen x noktası ve d yönü için optimum adım büyüklüğü alpha'yı bulur."""
        alphas = np.arange(0.0001, 1.0, 0.0001)
        f_values = [self.func(x + a * d) for a in alphas]
        return alphas[np.argmin(f_values)]

    def solve(self):
        x = self.x0.copy()

        # Döngü öncesi hazırlık: ilk gradyent, ilk yön ve norm
        g = self.grad(x)
        d = -g  # İlk iterasyonda en dik iniş ile aynı (beta=0)
        g_norm_prev = np.linalg.norm(g)

        for i in range(self.max_iter):
            grad = self.grad(x)
            # Gradyentin normunu yani büyüklüğünü hesapla; toleranstan küçükse optimuma ulaşılmış demektir, döngüyü durdur.
            g_norm = np.linalg.norm(grad)
            if g_norm < self.tol:
                break

            # Eşlenik yön hesabı: beta = (||g_t|| / ||g_t-1||)^2
            if i == 0:
                d = -grad  # İlk adımda beta yok, en dik iniş yönü
            else:
                beta = (g_norm / g_norm_prev) ** 2
                d = -grad + beta * d  # Eşlenik yön güncelleme

            g_norm_prev = g_norm

            alpha = self._line_search(x, d)
            x = x + alpha * d
            self.history.append(x.copy())
        return x


# Örnek 1.2 (Arora, 1989)
# f(x1, x2, x3) = x1^2 + 2*x2^2 + 2*x3^2 + 2*x1*x2 + 2*x2*x3
# Başlangıç noktası: (2, 4, 10)

if __name__ == "__main__":
    # Fonksiyon tanımı
    def func(x):
        return x[0]**2 + 2*x[1]**2 + 2*x[2]**2 + 2*x[0]*x[1] + 2*x[1]*x[2]

    # Gradyent tanımı: df/dx1 = 2x1+2x2, df/dx2 = 4x2+2x1+2x3, df/dx3 = 4x3+2x2
    def grad(x):
        return np.array([
            2*x[0] + 2*x[1],
            4*x[1] + 2*x[0] + 2*x[2],
            4*x[2] + 2*x[1]
        ])

    # Başlangıç noktası
    x0 = [2, 4, 10]

    # Sınıfı oluştur ve çöz
    cg = ConjugateGradient(func=func, grad=grad, x0=x0)
    sonuc = cg.solve()

    print(f"Optimum nokta    : x = {sonuc}")
    print(f"Fonksiyon değeri : f(x) = {func(sonuc):.6f}")
    print(f"İterasyon sayısı : {len(cg.history)}")
