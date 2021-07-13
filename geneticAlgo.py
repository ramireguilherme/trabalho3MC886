import random
from pacman import runGames
import numpy as np
class genetic():
    def __init__(self,popsize,crossover_rate,mutation_rate):
        self.popsize = popsize
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def generate_initial_pop(self, pop_size, gene_size):
        """
        
        """
        individuals = []
        for __ in len(pop_size):
            p = [random.randint(0,100) for i in range(gene_size)]
            individuals.append(p)
            p[0] = random.randint(1,20)
        return individuals

    def next_generation(self,parents):
        
        if random.randrange(100) < self.crossover_rate:
            self.crossover(,,)
        if random.randrange(100) < self.mutation_rate:
            self.mutation()
    def train(self):
        individuals = self.generate_initial_pop(10,35)
        for generation in self.generations:
            for individual in individuals:
                games = runGames(layout, individual, ghosts = 2, display, numGames, record, numTraining = 0, catchExceptions=False, timeout=30 )

    def crossover(self,geneA,geneB,x):
        geneA_new = np.append(geneA[:x],geneB[x:])
        geneB_new = np.append(geneB[:x],geneA[x:])

        return geneA_new,geneB_new
    
    def mutation(self,gene):
        mutation = random.randint(0,gene.size)
        gene[mutation] = random.randint(0,gene.size)
        return gene