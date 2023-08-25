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
    def UpdatePopulationFitness(pool, stu_list, proj_list, sup_list):
        # clear the existing rank and crowding distance
        for individual in pool:
            individual.Rank = -1
            individual.CrowdingDistance = -1

        MultiObjectiveHelper.CalculateSupervisorsFitness(pool, proj_list, sup_list)
        MultiObjectiveHelper.CalculateStudentsFitness(pool, stu_list)
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
    def CalculateStudentsFitness(pool, stu_list):
        for individual in pool:
            selectedProjectsRank = [0, 0, 0, 0, 0]
            individual_genes = individual.getGenes()
            for i in range(len(individual_genes)):
                stu_proj_preference_list = stu_list[i].getProjectList()
                #         check if the student chose this project and get the rank
                if individual_genes[i] in stu_proj_preference_list:
                    proj_rank = stu_proj_preference_list.index(individual_genes[i])
                    # print('project_rank', proj_rank)
                    selectedProjectsRank[proj_rank] += 1
            individual.All_Project_Ranks = selectedProjectsRank
            studentFitness = 65536 * selectedProjectsRank[0] \
                             + 256 * selectedProjectsRank[1] \
                             + 16 * selectedProjectsRank[2] + \
                             4 * selectedProjectsRank[3] \
                             + 2 * selectedProjectsRank[4]
            individual.StudentsFitness = studentFitness + 1

    @staticmethod
    def CalculateSupervisorsFitness(pool, proj_list, sup_list):
        for individual in pool:
            selectedSupervisorsAndNum = {}
            individual_genes = individual.getGenes()
            oversubscribedProjectIDAndSupervisors = {}
            satisfactionOfSupervisors = 0
            for i in range(len(individual_genes)):
                sup_id = proj_list[individual_genes[i]].getSupervisor()
                if sup_id not in selectedSupervisorsAndNum:
                    selectedSupervisorsAndNum.update({sup_id: [individual_genes[i]]})
                else:
                    existing_projectlist = selectedSupervisorsAndNum[sup_id]
                    existing_projectlist.append(individual_genes[i])
                    selectedSupervisorsAndNum.update({sup_id: existing_projectlist})
                # cur_num = len(selectedSupervisorsAndNum.get(sup_id))
                cur_num = len(selectedSupervisorsAndNum[sup_id])
                quota = sup_list[sup_id].quota
                if cur_num > quota:
                    # print('exceeds quota!')
                    if sup_id not in oversubscribedProjectIDAndSupervisors.keys():
                        oversubscribedProjectIDAndSupervisors.update({sup_id: [sup_id]})
                #     else:
                #         unavailableProjectList = oversubscribedProjectIDAndSupervisors.get(sup_id)
                #         unavailableProjectList.append(individual_genes[i])
                #         oversubscribedProjectIDAndSupervisors.update({sup_id: unavailableProjectList})

            # while len(oversubscribedProjectIDAndSupervisors) > 0:
            #     MultiObjectiveHelper.RepairChromosome(individual, oversubscribedProjectIDAndSupervisors, proj_list)
            #     MultiObjectiveHelper.CalculateSupervisorsFitness(pool, proj_list, sup_list)

            fitness_workload = 0
            fitness_satisfaction = 0
            if len(oversubscribedProjectIDAndSupervisors) > 0:
                individual.SupervisorsFitness = 0 - len(oversubscribedProjectIDAndSupervisors)
                continue
            else:
                for sup, selected_proj_list in selectedSupervisorsAndNum.items():
                    quota = sup_list[sup].getQuota()
                    cur_stu_num = len(selected_proj_list)
                    if cur_stu_num > quota:
                        fitness_workload = 0 - len(oversubscribedProjectIDAndSupervisors)
                        break
                    else:
                        if cur_stu_num <= quota / 2 + 1:
                            fitness_workload = fitness_workload + (cur_stu_num * 10) ^ 2
                        else:
                            fitness_workload = fitness_workload + cur_stu_num

                        sup_preference_list = sup_list[sup].getProjectList()

                        for proj in selected_proj_list:
                            rank = sup_preference_list.index(proj)
                            fitness_satisfaction = fitness_satisfaction + ((5 - rank) * 4) ^ 2
            individual.SupervisorsFitness = fitness_satisfaction + fitness_workload
            individual.SelectedSupervisorsAndProjects = selectedSupervisorsAndNum

    # @staticmethod
    # def RepairChromosome(individual, oversubscribedProjectIDAndSupervisors, proj_list):
    #     oversubscribedSupervisors = oversubscribedProjectIDAndSupervisors.values()
    #     unavailableProjects = oversubscribedProjectIDAndSupervisors.keys()
    #
    #     for i in range(len(individual)):
    #         project = individual[i]
    #         if project in unavailableProjects:
    #             MultiObjectiveHelper.generate_available_project(project, oversubscribedSupervisors, proj_list)
    #
    # @staticmethod
    # def generate_available_project(oversubscribedSupervisors, proj_list):
    #     return None

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
            if (anotherIndividual.StudentsFitness > individual.StudentsFitness \
                and anotherIndividual.SupervisorsFitness >= individual.SupervisorsFitness) \
                    or (anotherIndividual.StudentsFitness >= individual.StudentsFitness \
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