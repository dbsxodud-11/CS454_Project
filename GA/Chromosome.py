from copy import deepcopy
import random

class Chromosome :

    def __init__(self, chromosome_len) :

        self.value = [random.randint(0, 9) for _ in range(chromosome_len)]
        self.fitnessValues = {} # fitness function -> fitness value
        self.rank = 0

    def getFitness(self, fitness_function) :

        assert fitness_function in self.fitnessValues, "invalid fitness function"

        return self.fitnessValues.get(fitness_function)

    def clone(self) :
        return deepcopy(self)

    def size(self) :
        return len(self.value)

    def mutate(self, mutation_rate) :

        # Uniform Mutation
        for i in range(len(self.value)) :
            if random.random() <= mutation_rate :
                self.value[i] = random.randint(0, 9)

    def setFitness(self, fitness_function, operators) :
        
        fitness = self.value[0] # fitness value : maximum value by calculation
        for i in range(len(self.value)-1) :
            if operators[i] == 0 :
                fitness += self.value[i+1]
            elif operators[i] == 1 :
                fitness *= self.value[i+1]
            else :
                fitness -= self.value[i+1]
        
        self.fitnessValues[fitness_function] = fitness

    def getFitness(self, fitness_function) :
        return self.fitnessValues.get(fitness_function)

    def setRank(self, rank) :
        self.rank = rank
        