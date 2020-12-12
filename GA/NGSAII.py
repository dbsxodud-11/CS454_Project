from Chromosome import Chromosome
from Crossover import SinglePointCrossOver
from FitnessFunction import TSPFitnessFunction
from Ranking import CrowdingDistance, FastNonDominatedSorting
from Selection import TournamentSelection
from Genetic_Algorithm import GeneticAlgorithm

import random
import math

class NGSAII(GeneticAlgorithm) :

    def __init__(self, budget, node_list, position_list, delivery_list, traffic_list) :
        super().__init__(budget, node_list, position_list, delivery_list, traffic_list) 

        self.budget = budget
        self.node_list = node_list
        self.position_list = position_list
        self.delivery_list = delivery_list
        self.traffic_list = traffic_list

        self.selectionFunction = TournamentSelection()
        self.rankingFunction = FastNonDominatedSorting()
        self.crowdingDistance = CrowdingDistance()

    def evolve(self) :

        offspring_population = []
        
        for i in range(len(self.population)//2) :
            # Selection
            parent1 = self.selectionFunction.select(self.population)
            parent2 = self.selectionFunction.select(self.population)

            # Create Offsprings
            offspring1 = parent1.clone()
            offspring2 = parent2.clone()

            # Crossover
            # if random.random() <= self.crossover_rate :
            #     self.crossoverFunction.crossover(offspring1, offspring2)
            
            # Mutation
            offspring1.mutate(self.mutation_rate)
            offspring2.mutate(self.mutation_rate)

            # Evaluate
            for fitness_function in self.fitnessFunctions :
                fitness_function.getFitness(offspring1)
                fitness_function.getFitness(offspring2)

            # Add Offsprings to Offspring Population
            offspring_population.append(offspring1)
            offspring_population.append(offspring2)

            # Create the population union of Population and Offspring
            union = self.population + offspring_population

            # for i in range(len(union)) :
            #     for j in range(len(self.fitnessFunctions)) :
            #         print(union[i].getFitness(self.fitnessFunctions[j]))

            # Ranking the Union - Fast-NonDominted-Sort
            self.rankingFunction.computeRankingAssignment(union, self.fitnessFunctions)

            # Obtain Next Generation
            remain = len(self.population)
            idx = 0
            front = []
            self.population = []

            front = self.rankingFunction.getSubFront(idx)

            while remain > 0 and remain >= len(front) :
                # Crowding-Distance-Assignment
                self.crowdingDistance.crowdingDistanceAssignment(front, self.fitnessFunctions)
                self.population.extend(front)

                # Decrement remain
                remain -= len(front)
                
                # Obtain next front
                idx += 1
                if remain > 0 :
                    front = self.rankingFunction.getSubFront(idx)
            
            if remain > 0 :
                self.crowdingDistance.crowdingDistanceAssignment(front, self.fitnessFunctions)
                front = sorted(front, key=lambda x : (x.getRank(), x.getDistance()))

                for k in range(remain) :
                    self.population.append(front[k])
                remain = 0

        self.step += 1


if __name__ == "__main__" :

    import tsplib95

    problem = tsplib95.load("att48.tsp")
    node_position = problem.as_name_dict().get("node_coords")

    node_list = list(node_position.keys())
    position_list = list(node_position.values())
    delivery_list = [random.randint(1, 5) for _ in range(len(node_list))]
    traffic_list = [random.random()*0.5 + 1.0 for _ in range(len(node_list))]
    budget = 1000

    NSGA_II = NGSAII(budget, node_list, position_list, delivery_list, traffic_list)
    NSGA_II.generate_solution()