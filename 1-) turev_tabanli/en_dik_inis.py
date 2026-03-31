import numpy as np

class SteepestDescent:
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
        for i in range(self.max_iter):
            grad = self.grad(x)
            # Gradyentin normunu yani büyüklüğünü hesapla; toleranstan küçükse optimuma ulaşılmış demektir, döngüyü durdur.
            if np.linalg.norm(grad) < self.tol:
                break
            d = -grad
            alpha = self._line_search(x, d)
            x = x + alpha * d
            self.history.append(x.copy())
        return x



# Örnek 1.1 (Arora, 1989)
# f(x1, x2) = x1^2 + x2^2 - 2*x1*x2
# Başlangıç noktası: (1, 0)
# Beklenen sonuç: x_opt = (0.5, 0.5)


if __name__ == "__main__":
    # Fonksiyon tanımı
    def f(x):
        return x[0]**2 + x[1]**2 - 2 * x[0] * x[1]

    # Gradyent tanımı: df/dx1 = 2x1 - 2x2, df/dx2 = 2x2 - 2x1
    def grad(x):
        return np.array([2 * x[0] - 2 * x[1], 2 * x[1] - 2 * x[0]])

    # Başlangıç noktası
    x0 = [1, 0]

    # Sınıfı oluştur ve çöz
    sd = SteepestDescent(func=f, grad=grad, x0=x0)
    sonuc = sd.solve()

    print(f"Optimum nokta  : x = {sonuc}")
    print(f"Fonksiyon değeri: f(x) = {f(sonuc):.6f}")
    print(f"İterasyon sayısı: {len(sd.history)}")

