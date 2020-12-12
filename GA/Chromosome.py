from copy import deepcopy
import random

class Chromosome :

    def __init__(self, chromosome_len) :

        self.path = self.getRandomPath(chromosome_len) # random path
        self.fitnessValues = {} # fitness function -> fitness value
        self.rank = 0
        self.distance = 0.0

    def __len__(self) :
        return len(self.path)

    def getRandomPath(self, chromosome_len) :

        subpath = [i+1 for i in range(1, chromosome_len-1)]
        random.shuffle(subpath)

        return [1] + subpath + [1]

    def getFitness(self, fitness_function) :

        assert fitness_function in self.fitnessValues, "invalid fitness function"

        return self.fitnessValues.get(fitness_function)

    def clone(self) :
        return deepcopy(self)

    def size(self) :
        return len(self.path)

    def mutate(self, mutation_rate) :

        # Uniform Mutation
        for i in range(len(self.path)) :
            if random.random() <= mutation_rate :
                temp = self.path[i]
                point = random.randint(1, len(self.path)-2)
                self.path[i] = self.path[point]
                self.path[point] = temp

    def setFitness(self, fitness_function, fitness_value) :
        
        self.fitnessValues[fitness_function] = fitness_value

    def setRank(self, rank) :
        self.rank = rank
    
    def getRank(self) :
        return self.rank

    def setDistance(self, distance) :
        self.distance = distance

    def getDistance(self) :
        return self.distance

    def getFitnessValues(self) :
        distance, travel_time, score = list(self.fitnessValues.values())[0]

        return distance * 0.01 + travel_time - score * 50

        