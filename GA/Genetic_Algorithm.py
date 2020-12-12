from Chromosome import Chromosome
from Ranking import RankingFunction, FastNonDominatedSorting
from Crossover import SinglePointCrossOver
from Selection import RankSelection
from FitnessFunction import TSPFitnessFunction

import random

class GeneticAlgorithm :
    
    def __init__(self, budget, node_list, position_list, delivery_list, traffic_list) :

        self.budget = budget
        self.node_list = node_list
        self.position_list = position_list
        self.delivery_list = delivery_list
        self.traffic_list = traffic_list

        self.fitnessFunctions = []
        self.selectionFunction = RankSelection()
        self.crossoverFunction = SinglePointCrossOver()
        self.rankingFunction = RankingFunction()
        self.population = []
        self.step = 0
        self.population_size = 20
        self.crossover_rate = 0.2
        self.mutation_rate = 0.25
        self.chromosome_len = 48

    def setFitnessFunctions(self) :
        
        self.fitnessFunctions.append(TSPFitnessFunction(self.position_list, self.traffic_list, self.delivery_list))

    def init_population(self) :
        
        # Set Fitness Functions
        self.setFitnessFunctions()
        
        # Initialize Population
        for _ in range(self.population_size) :
            chromosome = Chromosome(self.chromosome_len)
            for fitness_function in self.fitnessFunctions :
                fitness_function.getFitness(chromosome)
            # print(chromosome.getFitnessValues())
            self.population.append(chromosome)


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

            # Ranking the Union
            self.rankingFunction.computeRankingAssignment(union, self.fitnessFunctions)

            # Obtain Next Generation(Rank Based Only)
            self.population = sorted(union, key = lambda x : x.rank)[:self.population_size]
            
        self.step += 1  

    def generate_solution(self) :

        performance_list = []
        if len(self.population) == 0 :
            self.init_population()
        
        # check initial state
        best_individual = sorted(self.population, key=lambda x : x.getFitness(self.fitnessFunctions[0]))[0]
        # print("----------------------Initial Soltion---------------------------------")
        # distance, travel_time, score = best_individual.getFitness(self.fitnessFunctions[0])
        # print(f"Distance : {distance}")
        # print(f"Travel Time : {travel_time}")
        # print(f"Score : {-score}")
        performance_list.append(best_individual.getFitness(self.fitnessFunctions[0]))

        while not self.isFinished() :
            self.evolve()
            best_individual = sorted(self.population, key=lambda x : x.getFitness(self.fitnessFunctions[0]))[0]
            performance_list.append(best_individual.getFitness(self.fitnessFunctions[0]))

        # check solution
        best_individual = sorted(self.population, key=lambda x : x.getFitness(self.fitnessFunctions[0]))[0]
        print("----------------------Final Solution---------------------------------")
        distance, travel_time, score = best_individual.getFitness(self.fitnessFunctions[0])
        print(f"Distance : {distance}")
        print(f"Travel Time : {travel_time}")
        print(f"Score : {-score}")
        performance_list.append(best_individual.getFitness(self.fitnessFunctions[0]))

        return performance_list

    def isFinished(self) :

        return self.step >= self.budget
        



if __name__ == "__main__" :

    import tsplib95

    problem = tsplib95.load("att48.tsp")
    node_position = problem.as_name_dict().get("node_coords")

    node_list = list(node_position.keys())
    position_list = list(node_position.values())
    delivery_list = [random.randint(1, 5) for _ in range(len(node_list))]
    traffic_list = [random.random()*0.5 + 1.0 for _ in range(len(node_list))]
    budget = 1000
    genetic_algorithm = GeneticAlgorithm(budget, node_list, position_list, delivery_list, traffic_list)
    genetic_algorithm.generate_solution()