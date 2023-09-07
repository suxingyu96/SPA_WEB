import copy
import pygame
from pygame import Vector2 as v2
from itertools import groupby
from operator import attrgetter
from algo.Slice import Slice

class MultiObjectiveHelper:
    # Update Population Fitness - Takes in a population of individuals,
    # and calculates their rank and crowding distances.
    # The set of individuals to have their rank and crowding distance calculated.
    @staticmethod
    # def UpdatePopulationFitness(pool, stu_list, proj_list, sup_list):
    def UpdatePopulationFitness(pool):
        # clear the existing rank and crowding distance
        for individual in pool:
            individual.Rank = -1
            individual.CrowdingDistance = -1

        # MultiObjectiveHelper.CalculateSupervisorsFitness(pool, proj_list, sup_list)
        # MultiObjectiveHelper.CalculateStudentsFitness(pool, stu_list)
        MultiObjectiveHelper.NormalizeFitnessValues(pool)

        remainingToBeRanked = copy.deepcopy(pool)
        rank = 1
        while len(remainingToBeRanked) > 0:
            individualsInRank = []

            for i in range(len(remainingToBeRanked)):
                individual = remainingToBeRanked[i]

                if MultiObjectiveHelper.isNotDominated(individual, remainingToBeRanked):
                    index = pool.index(individual)
                    pool[index].Rank = rank
                    individual.Rank = rank
                    individualsInRank.append(individual)

            for i in individualsInRank:
                remainingToBeRanked.remove(i)

            rank = rank + 1
        sorted_pool = sorted(pool, key=lambda x: x.Rank)

        ranks = []
        for k, g in groupby(sorted_pool, lambda x: x.Rank):
            ranks.append(list(g))
        # ranks = [list(result) for key, result in groupby(
        #     pool, key=lambda chromosome: chromosome.Rank)]
        for singleRank in ranks:
            MultiObjectiveHelper.CalculateCrowdingDistance(singleRank)

        return sorted_pool
    
    @staticmethod
    def NormalizeFitnessValues(pool):
        maxStudentsFitness = max(pool, key=attrgetter('StudentsFitness')).StudentsFitness
        maxSupervisorFitness = max(pool, key=attrgetter('SupervisorsFitness')).SupervisorsFitness

        for individual in pool:
            individual.NormalizedStudentsFitness = individual.StudentsFitness / maxStudentsFitness
            individual.NormalizedSupervisorsFitness = individual.SupervisorsFitness / maxSupervisorFitness

    @staticmethod
    def isNotDominated(individual, remainingToBeRanked):
        for anotherIndividual in remainingToBeRanked:
            if individual == anotherIndividual:
                continue
            # if anotherIndividual.StudentsFitness > individual.StudentsFitness:
            #         if the 'anotherIndividual' is better than 'individual' at least one objective
            #         and equal in other objectives
            if (anotherIndividual.StudentsFitness > individual.StudentsFitness
                and anotherIndividual.SupervisorsFitness >= individual.SupervisorsFitness) \
                    or (anotherIndividual.StudentsFitness >= individual.StudentsFitness
                        and anotherIndividual.SupervisorsFitness > individual.SupervisorsFitness):
                return False
        return True

    @staticmethod
    def CalculateCrowdingDistance(singleRank):
        sortedIndividuals = sorted(singleRank, key=lambda individual: individual.NormalizedStudentsFitness)
        individualsInFront = len(sortedIndividuals)

        for i in range(individualsInFront):
            # if the individual is the first one or the last one, it should have infinite crowding distance
            if i == 0 or i == individualsInFront - 1:
                sortedIndividuals[i].CrowdingDistance = float('inf')
            else:
                currentIndividual = sortedIndividuals[i]
                leftIndividual = sortedIndividuals[i - 1]
                rightIndividual = sortedIndividuals[i + 1]

                # Get the position on the fitness graph where studentFitness is the X axis,
                # supervisorsFitness is the Y axis
                currentPosition = v2(currentIndividual.NormalizedStudentsFitness,
                                     currentIndividual.NormalizedSupervisorsFitness)
                leftPosition = v2(leftIndividual.NormalizedStudentsFitness,
                                  leftIndividual.NormalizedSupervisorsFitness)
                rightPosition = v2(rightIndividual.NormalizedStudentsFitness,
                                   rightIndividual.NormalizedSupervisorsFitness)

                distanceLeft = pygame.math.Vector2.distance_to(currentPosition, leftPosition)
                distanceRight = pygame.math.Vector2.distance_to(currentPosition, rightPosition)

                sortedIndividuals[i].CrowdingDistance = distanceLeft + distanceRight

    @staticmethod
    def CalculateArea(bestIndividuals):
        slice_list = MultiObjectiveHelper.getSlices(bestIndividuals)
        sum_area = 0
        for slice in slice_list:
            sum_area += slice.Area

        return sum_area

    @staticmethod
    def getSlices(Individuals):
        preSlice = Slice(0, 0, 0, 0)
        slices = []

        for i in Individuals:
            preSlice = Slice(i.SupervisorsFitness, preSlice.XUpper, i.StudentsFitness, 0)
            slices.append(preSlice)

        return slices
