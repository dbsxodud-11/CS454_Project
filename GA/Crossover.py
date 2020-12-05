import random

class CrossOverFunction :

    def __init__(self) :
        pass

    def crossover(self, offspring1, offspring2) :
        pass

class SinglePointCrossOver(CrossOverFunction) :

    def __init__(self) :
        super(SinglePointCrossOver, self).__init__()

    def crossover(self, offspring1, offspring2) :

        if offspring1.size() < 2 or offspring2.size() < 2 :
            return
        
        point1 = random.randint(0, offspring1.size()-1)
        point2 = random.randint(0, offspring2.size()-1)

        # single point crossover
        temp = offspring1.value[point1]
        offspring1.value[point1] = offspring2.value[point2]
        offspring2.value[point2] = temp


