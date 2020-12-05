import random

class FitnessFunction :

    def __init__(self) :
        pass

    def getFitness(self, chromosome) :
        pass

class RandomCalculationFitnessFunction(FitnessFunction) : # find maximum value with fixed random operators

    def __init__(self, chromosome_len) :
        super(RandomCalculationFitnessFunction, self).__init__()
        
        # random operator sequence
        self.operators = [random.randint(0, 2) for _ in range(chromosome_len-1)]

    def getFitness(self, chromosome) :

        chromosome.setFitness(self, self.operators)