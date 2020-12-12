from copy import deepcopy
import sys

class RankingFunction :

    def __init__(self) :
        pass

    def computeRankingAssignment(self, population, fitnessFunctions) :

        # compute rank solely on average of fitness value
        rank = []
        for i in range(len(population)) :
            fitness_average = population[i].getFitness(fitnessFunctions[0])
            # for fitness_function in fitnessFunctions : 
            #     fitness_average += population[i].getFitnessValues()
            # print(fitness_average)
            rank.append((i, fitness_average))

        rank = sorted(rank, key=lambda x: x[1])
        start = 1
        for i in rank :
            population[i[0]].setRank(start)
            start += 1

class FastNonDominatedSorting(RankingFunction) : 

    def __init__(self) :
        super(FastNonDominatedSorting, self).__init__()
        self.ranking = []

    def computeRankingAssignment(self, union, fitnessFunctions) :

        self.ranking = self.getNextNonDominatedFronts(union, fitnessFunctions)
        # self.ranking = deepcopy(fronts)

    def getNextNonDominatedFronts(self, union, fitnessFunctions) :

        criterion = DominanceComparator(fitnessFunctions)

        dominateMe = [0 for _ in range(len(union))]
        iDominate = [[] for _ in range(len(union))]
        front = [[] for _ in range(len(union)+1)]
        flag = False
        
        for individual in union :
            individual.setDistance(sys.float_info.max) 

        # Fast-Non-Dominated-Sorting Algorithm
        for p in range(len(union)-1) :
            for q in range(p+1, len(union)) :
                flag = criterion.compare(union[p], union[q])

                if flag == -1 :
                    iDominate[p].append(q)
                    dominateMe[q] += 1
                elif flag == 1 :
                    iDominate[q].append(p)
                    dominateMe[p] += 1
        
        for p in range(len(union)) :
            if dominateMe[p] == 0 : # p belongs to the first front
                front[0].append(p)
                union[p].setRank(1)

        # Rest of Fronts
        i = 0
        while len(front[i]) > 0 :
            i += 1
            for j in front[i-1] :
                for k in iDominate[j] :
                    dominateMe[k] -= 1
                    if dominateMe[k] == 0 :
                        front[i].append(k)
                        union[k].setRank(i+1)

        fronts = [[] for _ in range(i)]
        for j in range(i) :
            for k in front[j] :
                fronts[j].append(union[k])

        return fronts
    
    def getSubFront(self, rank) :
        return self.ranking[rank]


class DominanceComparator :

        def __init__(self, fitnessFunctions) :
            
            self.fitnessFunctions = fitnessFunctions

        def compare(self, a, b) :

            if a is None :
                return 1
            elif b is None :
                return -1

            dominate_1 = False
            dominate_2 = False

            for i in range(3) :
                
                flag = a.getFitness(self.fitnessFunctions[0])[0] < b.getFitness(self.fitnessFunctions[0])[0]

            if flag :
                dominate_1 = True
                if dominate_2 : # Non-Dominated
                    return 0
            else :
                dominate_2 = True
                if dominate_1 :
                    return 0

            if dominate_1 == dominate_2 :
                return 0
            elif dominate_1 :
                return -1 # a dominates
            else :
                return 1 # b dominates


class CrowdingDistance :

    def __init__(self) :
        pass

    def crowdingDistanceAssignment(self, front, fitnessFunctions) :

        if len(front) == 0 :
            return
        elif len(front) == 1 :
            front[0].setDistance(sys.float_info.max)
            return
        elif len(front) == 2 :
            front[0].setDistance(sys.float_info.max)
            front[1].setDistance(sys.float_info.max)
            return
        else :
            for i in range(len(front)) :
                front[i].setDistance(0.0)
            

            front[0].setDistance(0.0)
            objectiveMaxn = 0.0
            objectiveMinn = 0.0
            distance = 0.0

            for i in range(len(self.fitnessFunctions)) :
                
                # Sort Fitness by Fitness Function  
                # for i in range(len(front)) :
                #     print(front[i].getFitness(fitness_function))
                front = list(sorted(front, key = lambda x: x.getFitness(fitnessFunctions[i])[i]))
                objectiveMinn = front[0].getFitness(fitnessFunctions[0])[i]
                objectiveMaxn = front[-1].getFitness(fitnessFunctions[0])[i]

                front[0].setDistance(sys.float_info.max)
                front[-1].setDistance(sys.float_info.max)

                for j in range(1, len(front)-1) :
                    # Calculte Crowding Distance
                    distance = front[j+1].getFitness(fitnessFunctions[0])[i] - front[j-1].getFitness(fitnessFunctions[0])[i]
                    distance /= objectiveMaxn - objectiveMinn
                    distance += front[j].getDistance()
                    front[j].setDistance(distance)


