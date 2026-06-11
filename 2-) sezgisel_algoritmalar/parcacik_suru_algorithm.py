import random

# =============================================================================
# PARCACIK SURU OPTIMIZASYONU (Particle Swarm Optimization - PSO)
# -----------------------------------------------------------------------------
# PSO; kus suruleri veya balik suruleri gibi topluluklarin yiyecek ararken
# sergiledikleri sosyal davranistan esinlenen, populasyon tabanli bir
# sezgisel (heuristic) optimizasyon yontemidir.
#
# Her bir "parcacik" arama uzayinda olasi bir cozumu temsil eder ve uzayda
# bir konuma (position) ve hiza (velocity) sahiptir. Parcaciklar hem kendi
# gecmis en iyi konumlarini (kisisel deneyim) hem de surunun bulduğu en iyi
# konumu (sosyal deneyim) kullanarak hareketlerini gunceller.
# =============================================================================


class PSO:
    def __init__(self, num_particles, num_dimensions, inertia_weight=0.5, cognitive_weight=1.0, social_weight=1.0):
        self.num_particles = num_particles        # Surudeki parcacik sayisi
        self.num_dimensions = num_dimensions       # Problemin boyut sayisi (degisken adedi)
        self.inertia_weight = inertia_weight       # w: Atalet agirligi (onceki hizi koruma egilimi)
        self.cognitive_weight = cognitive_weight   # c1: Bilissel agirlik (kisisel deneyime guven)
        self.social_weight = social_weight         # c2: Sosyal agirlik (surunun deneyimine guven)

        # Parcaciklarin konum ve hizlarini baslat
        self.positions = [[0.0 for _ in range(num_dimensions)] for _ in range(num_particles)]
        self.velocities = [[0.0 for _ in range(num_dimensions)] for _ in range(num_particles)]
        self.personal_best_positions = [[0.0 for _ in range(num_dimensions)] for _ in range(num_particles)]
        self.personal_best_scores = [float('inf') for _ in range(num_particles)]
        self.global_best_position = [0.0 for _ in range(num_dimensions)]
        self.global_best_score = float('inf')

    def initialize(self, bounds):
        """
        Parcaciklari arama uzayinda rastgele baslatir.
        bounds: her boyut icin (alt_sinir, ust_sinir) ikililerinden olusan liste.
        """
        for i in range(self.num_particles):
            for d in range(self.num_dimensions):
                lower, upper = bounds[d]
                # Konum: arama uzayi sinirlari icinde rastgele
                self.positions[i][d] = random.uniform(lower, upper)
                # Hiz: genellikle aralik genisliginin negatif/pozitif yarisi ile sinirli baslar
                span = upper - lower
                self.velocities[i][d] = random.uniform(-span, span)
            # Baslangicta kisisel en iyi = mevcut konum
            self.personal_best_positions[i] = list(self.positions[i])

    def optimize(self, objective_function, bounds, max_iterations):
        """
        PSO ana dongusu.
        objective_function: minimize edilecek amac fonksiyonu (kucuk = iyi).
        bounds: her boyut icin (alt_sinir, ust_sinir) listesi.
        max_iterations: iterasyon (jenerasyon) sayisi.
        """
        self.initialize(bounds)

        # --- Baslangic degerlendirmesi: kisisel ve global en iyileri hesapla ---
        for i in range(self.num_particles):
            score = objective_function(self.positions[i])
            self.personal_best_scores[i] = score
            if score < self.global_best_score:
                self.global_best_score = score
                self.global_best_position = list(self.positions[i])

        # --- Iterasyon dongusu ---
        for _ in range(max_iterations):
            for i in range(self.num_particles):
                for d in range(self.num_dimensions):
                    # r1 ve r2: [0,1] araliginda rastgele sayilar.
                    # Hareketi stokastik (rastgele) yaparak arama cesitliligi saglar.
                    r1 = random.random()
                    r2 = random.random()

                    # --- HIZ GUNCELLEME FORMULU ---
                    # v(t+1) = w*v(t) + c1*r1*(pBest - x) + c2*r2*(gBest - x)
                    #
                    #  w * v(t)                      -> Atalet terimi: parcacik onceki yonunu korur (kesif/exploration).
                    #  c1 * r1 * (pBest - x)         -> Bilissel terim: parcaciği kendi en iyi konumuna ceker.
                    #  c2 * r2 * (gBest - x)         -> Sosyal terim: parcaciği surunun en iyi konumuna ceker.
                    inertia = self.inertia_weight * self.velocities[i][d]
                    cognitive = self.cognitive_weight * r1 * (self.personal_best_positions[i][d] - self.positions[i][d])
                    social = self.social_weight * r2 * (self.global_best_position[d] - self.positions[i][d])
                    self.velocities[i][d] = inertia + cognitive + social

                    # --- KONUM GUNCELLEME FORMULU ---
                    # x(t+1) = x(t) + v(t+1)
                    # Yeni hiz, parcacigin yeni konumunu belirler.
                    self.positions[i][d] += self.velocities[i][d]

                    # Konumu arama uzayi sinirlari icinde tut (clamping)
                    lower, upper = bounds[d]
                    if self.positions[i][d] < lower:
                        self.positions[i][d] = lower
                    elif self.positions[i][d] > upper:
                        self.positions[i][d] = upper

                # --- Yeni konumu degerlendir ---
                score = objective_function(self.positions[i])

                # Kisisel en iyiyi guncelle (daha iyi cozum bulunduysa)
                if score < self.personal_best_scores[i]:
                    self.personal_best_scores[i] = score
                    self.personal_best_positions[i] = list(self.positions[i])

                # Global en iyiyi guncelle (tum sure icin en iyi cozum)
                if score < self.global_best_score:
                    self.global_best_score = score
                    self.global_best_position = list(self.positions[i])

        return self.global_best_position, self.global_best_score


# =============================================================================
# ORNEK KULLANIM
# =============================================================================
if __name__ == "__main__":
    # Amac fonksiyonu: Sphere fonksiyonu f(x) = sum(x_i^2)
    # Minimumu x = [0, 0, ...] noktasinda ve deger 0'dir.
    def sphere(x):
        return sum(xi ** 2 for xi in x)

    num_dimensions = 2
    bounds = [(-10, 10)] * num_dimensions  # Her boyut [-10, 10] araliginda

    pso = PSO(
        num_particles=30,
        num_dimensions=num_dimensions,
        inertia_weight=0.5,
        cognitive_weight=1.5,
        social_weight=1.5,
    )

    best_position, best_score = pso.optimize(sphere, bounds, max_iterations=100)

    print("En iyi konum :", best_position)
    print("En iyi deger :", best_score)
