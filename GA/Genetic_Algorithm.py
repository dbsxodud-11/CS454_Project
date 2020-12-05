from Chromosome import Chromosome
from Ranking import RankingFunction
from Crossover import SinglePointCrossOver
from Selection import RankSelection
from FitnessFunction import RandomCalculationFitnessFunction

import random

class GeneticAlgorithm() :
    
    def __init__(self) :

        self.fitnessFunctions = []
        self.numObjectives = 5
        self.selectionFunction = RankSelection()
        self.crossoverFunction = SinglePointCrossOver()
        self.rankingFunction = RankingFunction()
        self.population = []
        self.step = 0
        self.finish_step = 100
        self.population_size = 20
        self.crossover_rate = 0.2
        self.mutation_rate = 0.25
        self.chromosome_len = 10

    def setFitnessFunctions(self, num) :
        
        # Set Fitness Function for each objective
        for _ in range(num) :
            fitness_function = RandomCalculationFitnessFunction(self.chromosome_len)
            self.fitnessFunctions.append(fitness_function)

    def init_population(self) :
        
        # Set Fitness Functions
        self.setFitnessFunctions(self.numObjectives)
        
        # Initialize Population
        for _ in range(self.population_size) :
            chromosome = Chromosome(self.chromosome_len)
            for fitness_function in self.fitnessFunctions :
                fitness_function.getFitness(chromosome)
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
            if random.random() <= self.crossover_rate :
                self.crossoverFunction.crossover(offspring1, offspring2)
            
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

        if len(self.population) == 0 :
            self.init_population()
        
        # check initial state
        fitness_average = 0
        for j in range(len(self.fitnessFunctions)) :
            fitness_average += self.population[random.randint(0, len(self.population)-1)].getFitness(self.fitnessFunctions[j])
        fitness_average /= len(self.fitnessFunctions)
        print(fitness_average)

        while not self.isFinished() :
            self.evolve()

        # check solution
        fitness_average = 0
        for j in range(len(self.fitnessFunctions)) :
            fitness_average += self.population[random.randint(0, len(self.population)-1)].getFitness(self.fitnessFunctions[j])
        fitness_average /= len(self.fitnessFunctions)
        print(fitness_average)


    def isFinished(self) :

        return self.step >= self.finish_step
        



if __name__ == "__main__" :

    genetic_algorithm = GeneticAlgorithm()
    genetic_algorithm.generate_solution()