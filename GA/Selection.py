import random
import math

class SelectionFunction :

    def __init__(self) :
        pass

    def select(self, population) :
        pass

class RankSelection(SelectionFunction) :

    def __init__(self) :
        super(RankSelection, self).__init__()
        self.rank_bias = 1.5

    def select(self, population) :

        # Using GENITOR algorithm 
        r = random.random()
        d = self.rank_bias - math.sqrt(self.rank_bias**2 - (4.0*(self.rank_bias-1.0)*r))

        d = d/2.0/(self.rank_bias-1.0)
        idx = int(len(population) * d)

        return population[idx]
