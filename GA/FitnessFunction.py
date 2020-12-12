import random
import math

class FitnessFunction :

    def __init__(self) :
        pass

    def getFitness(self, chromosome) :
        pass

# class RandomCalculationFitnessFunction(FitnessFunction) : # find maximum value with fixed random operators

#     def __init__(self, chromosome_len) :
#         super(RandomCalculationFitnessFunction, self).__init__()
        
#         # random operator sequence
#         self.operators = [random.randint(0, 2) for _ in range(chromosome_len-1)]

#     def getFitness(self, chromosome) :

#         chromosome.setFitness(self, self.operators)

# class Distance(FitnessFunction) :

#     def __init__(self, position_list) :
#         super(Distance, self).__init__()

#         self.distance = 0
#         self.position_list = position_list
    
#     def getFitness(self, chromosome) :

#         for i in len(chromosome) :
#             if i == len(chromosome) - 1 :
#                 self.distance += distance(position_list[i], position_list[1])
#             else :
#                 self.distance += distance(position_list[i], position_list[i+1])

#         return self.distance

#     def distance(self, position1, position2) :

#         return math.sqrt((position1[0]-position2[1])**2 + (position1[0]-position[1])**2)

# class TravelTime(FitnessFunction) :

#     def __init__(self, position_list, traffic_list) :
#         super(TravelTime, self).__init__()

#         self.travel_time = 0
#         self.position_list = position_list
#         self.traffic_list = traffic_list

#     def getFitness(self, chromosome) :

#         for i in len(chromosome) :
#             if i == len(chromosome) - 1 :
#                 self.travel_time += travel_time(self.position_list[i], self.position_list[1], self.traffic_list[i], self.traffic_list[1])
#             else :
#                 self.travel_time += travel_time(self.position_list[i], self.position_list[i+1], self.traffic_list[i], self.traffic_list[i+1])

#         return self.travel_time

#     def travel_time(self, position1, position2, traffic1, traffic2) :

#         return math.sqrt((position1[0]-position2[1])**2 + (position1[0]-position[1])**2) * traffic1 * traffic2

# class Satisfication(FitnessFunction) :

#     def __init__(self, position_list, delivery_list) :
#         super(Satisfication, self).__init__()

#         self.rating = 0
#         self.position_list = position_list
#         self.delivery_list = delivery_list

#     def getFitness(self, chromosome) :

#         for i in len(chromosome)-2 :
#             self.rating = satisfication(self.position_list[i], self.position[i+1], self.delivery_list[i+1])

#         return self.rating / (len(chromosome)-1)

#     def satisfication(self, position1, position2, delivery) :
        

#         return 5*(math.exp(-delivery_list[solution[i+1]-1]*0.1*time))

class TSPFitnessFunction(FitnessFunction) :

    def __init__(self, position_list, traffic_list, delivery_list) :
        super(TSPFitnessFunction, self).__init__()

        self.position_list = position_list
        self.traffic_list = traffic_list
        self.delivery_list = delivery_list

    def getFitness(self, chromosome) :

        distance_fitness = 0
        travel_time_fitness = 0
        score_fitness = 0

        for i in range(1, len(chromosome)):
            distance = self.getDistance(self.position_list[chromosome.path[i-1]-1], self.position_list[chromosome.path[i]-1])
            travel_time = self.getTravelTime(distance, self.traffic_list[chromosome.path[i-1]-1], self.traffic_list[chromosome.path[i]-1])
            distance_fitness += distance
            travel_time_fitness += travel_time
            score_fitness -= self.getScore(self.delivery_list[chromosome.path[i]-1], travel_time_fitness)

        score_fitness /= len(chromosome)-1

        chromosome.setFitness(self, (distance_fitness, travel_time_fitness, score_fitness))
        # return distance_fitness, travel_time_fitness, score_fitness

    def getDistance(self, position_1, position_2) :

        return ((position_1[0]-position_2[0])**2 + (position_1[1]-position_2[1])**2)**0.5

    def getTravelTime(self, distance, traffic_1, traffic_2) :

        return (distance/1000)*traffic_1*traffic_2
    
    def getScore(self, reduce_ratio, time) :

        return -5*math.exp(-reduce_ratio*0.01*time)
