
class RankingFunction :

    def __init__(self) :
        pass

    def computeRankingAssignment(self, population, fitnessFunctions) :

        # compute rank solely on average of fitness value
        rank = []
        for i in range(len(population)) :
            fitness_average = 0
            for fitness_function in fitnessFunctions : 
                fitness_average += population[i].getFitness(fitness_function)
            rank.append((i, fitness_average / len(fitnessFunctions)))

        rank = sorted(rank, key=lambda x: -x[1]) # Descending Order
        start = 1
        for i in rank :
            population[i[0]].setRank(start)
            start += 1