import random as rd
import math
from importlib import util, import_module

cocoex = None
if util.find_spec("cocoex") is not None:
    cocoex = import_module("cocoex")

class GeneticAlgorithm:
    def __init__(
        self,
        population_size,
        mutation_rate,
        crossover_rate,
        roulette_wheel_selection=True,
        elitism_rate=0.1,
        dimension=2,
        bbob_instance=1,
        use_exact_bbob=True,
    ):
        if population_size <= 0:
            raise ValueError("population_size 0'dan buyuk olmalidir.")
        if not 0 <= mutation_rate <= 1:
            raise ValueError("mutation_rate 0 ile 1 arasinda olmalidir.")
        if not 0 <= crossover_rate <= 1:
            raise ValueError("crossover_rate 0 ile 1 arasinda olmalidir.")
        if not 0 <= elitism_rate <= 1:
            raise ValueError("elitism_rate 0 ile 1 arasinda olmalidir.")

        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.roulette_wheel_selection = roulette_wheel_selection
        self.elitism_rate = elitism_rate
        self.dimension = dimension
        self.population = []

        self.bbob_instance = bbob_instance
        self.use_exact_bbob = use_exact_bbob and cocoex is not None
        self.bbob_problem = None
        if self.use_exact_bbob:
            self.bbob_problem = cocoex.BareProblem(
                suite_name="bbob",
                function=15,
                dimension=self.dimension,
                instance=self.bbob_instance,
            )

    def decode_individual(self, individual, alt_sinir=-5.0, ust_sinir=5.0):
        # Kromozomu D parcaya bolup her parcayi reel degere cevirir.
        if len(individual) < self.dimension:
            raise ValueError("Kromozom uzunlugu dimension degerinden kucuk olamaz.")
        if len(individual) % self.dimension != 0:
            raise ValueError("gene_length, dimension degerine tam bolunmelidir.")

        bits_per_var = len(individual) // self.dimension

        def bits_to_real(bits):
            max_int = (1 << len(bits)) - 1
            int_val = int("".join(str(b) for b in bits), 2)
            return alt_sinir + (int_val / max_int) * (ust_sinir - alt_sinir)

        x = []
        for i in range(self.dimension):
            basla = i * bits_per_var
            bitir = (i + 1) * bits_per_var
            x.append(bits_to_real(individual[basla:bitir]))
        return x
    
    def initialize_population(self, gene_length):
        self.population = [
            [rd.randint(0, 1) for _ in range(gene_length)] 
            for _ in range(self.population_size)]
        
    def bbob_f15_rastrigin(self, x):
        # BBOB f15 icin kanonik Rastrigin fallback (transformsuz).
        d = len(x)
        toplam = 0.0
        for xi in x:
            toplam += xi ** 2 - 10 * math.cos(2 * math.pi * xi)
        return 10 * d + toplam

    def fitness(self, individual):
        # Literatur problemi: BBOB f15 (Rastrigin) minimizasyonu
        x = self.decode_individual(individual)

        if self.use_exact_bbob and self.bbob_problem is not None:
            return float(self.bbob_problem(x))

        return self.bbob_f15_rastrigin(x)

    def fitness_scaling(self):
        # Minimizasyonu secime uygun hale getirmek icin objective degerlerini tersleyip normalize eder.
        objective_values = [self.fitness(ind) for ind in self.population]
        max_obj = max(objective_values)
        min_obj = min(objective_values)
        eps = 1e-9

        if max_obj - min_obj < eps:
            return [1.0 for _ in objective_values]

        return [(max_obj - obj) / (max_obj - min_obj) + eps for obj in objective_values]
    
    def selection(self):
        scaled_fitness = self.fitness_scaling()

        if self.roulette_wheel_selection:
            total_fitness = sum(scaled_fitness)
            pick = rd.uniform(0, total_fitness)
            current = 0
            for ind, fit in zip(self.population, scaled_fitness):
                current += fit
                if current > pick:
                    return ind
            return self.population[-1]
        else:
            # Turnuva seçimi
            tournament_size = 3
            sample_size = min(tournament_size, len(self.population))
            sampled_indices = rd.sample(range(len(self.population)), sample_size)
            best_idx = max(sampled_indices, key=lambda i: scaled_fitness[i])
            return self.population[best_idx]
    def crossover(self, parent1, parent2):
        if rd.random() < self.crossover_rate:
            point = rd.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        else:
            return parent1, parent2
        
    def mutate(self, individual):
        for i in range(len(individual)):
            if rd.random() < self.mutation_rate:
                individual[i] = 1 - individual[i]  # Bit flip mutation
        return individual
    
    def run(self, gene_length, generations):
        if gene_length % self.dimension != 0:
            raise ValueError("gene_length, dimension degerine tam bolunmelidir.")

        self.initialize_population(gene_length)
        best_individual = min(self.population, key=self.fitness)
        
        for generation in range(generations):
            new_population = []
            elite_count = int(self.elitism_rate * self.population_size)
            new_population.extend(sorted(self.population, key=self.fitness)[:elite_count])
            
            while len(new_population) < self.population_size:
                parent1 = self.selection()
                parent2 = self.selection()
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                if len(new_population) < self.population_size:
                    new_population.append(self.mutate(child2))
            
            self.population = new_population
            current_best = min(self.population, key=self.fitness)
            if self.fitness(current_best) < self.fitness(best_individual):
                best_individual = current_best
        
        return best_individual, self.fitness(best_individual)
    
if __name__ == "__main__":
    ga = GeneticAlgorithm(
        population_size=100,
        mutation_rate=0.01,
        crossover_rate=0.7,
        elitism_rate=0.1,
        dimension=2,
        bbob_instance=1,
        use_exact_bbob=True,
    )
    best_solution, best_fitness = ga.run(gene_length=20, generations=50)
    if cocoex is None:
        print("Benchmark: BBOB f15 Rastrigin (canonical fallback, cocoex yok)")
    else:
        print(f"Benchmark: BBOB f15 Rastrigin (exact cocoex, instance={ga.bbob_instance})")
    print("Best Solution:", best_solution)
    print("Best Fitness:", best_fitness)
    
    
    
    