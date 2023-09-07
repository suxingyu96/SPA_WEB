import copy
import random
import statistics
import sys
import time
from math import inf
import numpy as np
from itertools import groupby
from algo.MultiObjectiveHelper import MultiObjectiveHelper
from algo.Chromosome import Chromosome
from algo.ParetoVisualScreen import ParetoVisualScreen
from algo.Slice import Slice


class SPA_genetic_algorithm:
    def __init__(self, stu_list, proj_list, sup_list, pool_size, mutate_rate, crossover_rate,
                 max_generations, max_noImprovementCount):
        self._numParents = pool_size
        self._mutate_rate = mutate_rate
        self._stu_list = stu_list
        self._proj_list = proj_list
        self._sup_list = sup_list
        self._geneSet = self.__create_gene_set()
        self._pool = self.generate_first_population()
        self._max_generations = max_generations
        self._max_noImprovementCount = max_noImprovementCount
        self._crossover_rate = crossover_rate
        self._best_students_fitness_record = []
        self._best_supervisors_fitness_record = []
        self._generation = 0

    def generate_first_population(self):
        lenOfgenes = len(self._stu_list)
        # pool = [self.generate_parent(self._geneSet, lenOfgenes) for _ in range(self._numParents)]
        pool = []
        while len(pool) < self._numParents:
            genes = self.generate_parent(self._geneSet, lenOfgenes)
            if genes not in pool:
                pool.append(genes)

        for i in range(len(pool)):
            genes = pool[i]
            individual = Chromosome(genes)
            pool[i] = individual
        return pool

    def run(self, paretoScreen, pool=None):
        if pool is not None:
            print(pool)
            self._pool = pool
        print('generation', self._generation)
        self.CalculateStudentsFitness(self._pool, self._stu_list)
        self.CalculateSupervisorsFitness(self._pool, self._proj_list, self._sup_list)
        # self._pool = MultiObjectiveHelper.UpdatePopulationFitness(self._pool, self._stu_list, self._proj_list, self._sup_list)
        self._pool = MultiObjectiveHelper.UpdatePopulationFitness(self._pool)

        if paretoScreen:
            paretoFrontWindow = ParetoVisualScreen()

        # Termination Condition
        isConverged = False
        NoImprovementCount = 0
        preConvergenceArea = 0
        bestIndividuals = []
        while not isConverged:
            if paretoScreen:
                paretoFrontWindow.Update(self._pool, self._generation)
                time.sleep(1)

            bestIndividuals = self.getBestIndividuals(self._pool)
            if self._generation % 4 == 0:
                if len(bestIndividuals) < 2:
                    if bestIndividuals[0].CrowdingDistance != float(inf):
                        exit
                    self.__record_current_fitness(bestIndividuals[0], bestIndividuals[0])
                else:
                    if bestIndividuals[0].CrowdingDistance != float(inf)\
                            or bestIndividuals[1].CrowdingDistance != float(inf):
                        exit
                    self.__record_current_fitness(bestIndividuals[0], bestIndividuals[1])
            sorted_bestIndividuals = sorted(bestIndividuals, key=lambda x: x.SupervisorsFitness)
            curArea = MultiObjectiveHelper.CalculateArea(sorted_bestIndividuals)
            if abs(curArea - preConvergenceArea) < 0.01 * preConvergenceArea:
                NoImprovementCount += 1
            else:
                NoImprovementCount = 0
                preConvergenceArea = curArea

            print("No.{0} Generation:".format(self._generation))
            print('The bests:', len(bestIndividuals))
            self.displayIndividuals(bestIndividuals)

            self._generation += 1

            # produce offspring
            offspring = self.generateOffspring()
            self.CalculateStudentsFitness(offspring, self._stu_list)
            self.CalculateSupervisorsFitness(offspring, self._proj_list, self._sup_list)
            self._pool.extend(offspring)
            self._pool = MultiObjectiveHelper.UpdatePopulationFitness(self._pool)

            # Sort all individuals and produce new population
            newPopulation = []
            sorted_pool = sorted(self._pool, key=lambda x: (x.Rank, 0 - x.CrowdingDistance))
            for i in sorted_pool:
                if i not in newPopulation and i.CrowdingDistance != 0:
                    newPopulation.append(i)
                if len(newPopulation) >= 0.7 * self._numParents:
                    break
            #
            while len(newPopulation) < self._numParents:
                randomIndividual = random.choice(sorted_pool)
                if randomIndividual not in newPopulation and randomIndividual.Rank != -1:
                    newPopulation.append(randomIndividual)

            self._pool.clear()
            self._pool = newPopulation
            print('no improvement count:', NoImprovementCount)
            isConverged = self._generation >= self._max_generations or NoImprovementCount > self._max_noImprovementCount
        return bestIndividuals

    def __record_current_fitness(self, individual_a, individual_b):
        best_supervisors_fitness = max(individual_a.SupervisorsFitness, individual_b.SupervisorsFitness)
        best_students_fitness = max(individual_a.StudentsFitness, individual_b.StudentsFitness)
        self._best_supervisors_fitness_record.append(best_supervisors_fitness)
        self._best_students_fitness_record.append(best_students_fitness)

    def get_records(self):
        return self._best_students_fitness_record, self._best_supervisors_fitness_record

    def __create_gene_set(self):
        geneSet = []
        for id, project in self._proj_list.items():
            project_id = id
            geneSet.append(project_id)

        return geneSet

    def generate_parent(self, geneSet, lenOfGenes):
        return random.sample(geneSet, lenOfGenes)

    def generateOffspring(self):
        offspring = []
        print('num of pool', len(self._pool))
        print('mutation rate:', self._mutate_rate)
        print('crossover rate:', self._crossover_rate)
        count = 0
        while len(offspring) < 0.8 * len(self._pool):
            rate = random.uniform(0, 1)
            children_genes = []
            if rate < self._crossover_rate:
            # crossover
            # parent = self.tournamentSelection()
            # donor = self.tournamentSelection()
                candidate_a, candidate_b = self.get_candidates(self._pool)
                parent = self.tournamentSelection(candidate_a, candidate_b)
                candidate_a, candidate_b = self.get_candidates(self._pool)
                donor = self.tournamentSelection(candidate_a, candidate_b)
                while parent == donor:
                    candidate_a, candidate_b = self.get_candidates(self._pool)
                    donor = self.tournamentSelection(candidate_a, candidate_b)
                start, end = self._generate_two_points(len(parent.getGenes()))
                # print('start and end', start, end)
                children_genes = []
                children_gene_a = self.crossover_PMX(parent.getGenes(), donor.getGenes(), start, end)
                children_gene_b = self.crossover_PMX(donor.getGenes(), parent.getGenes(), start, end)
            else:
                candidate_a, candidate_b = self.get_candidates(self._pool)
                children_gene_a = copy.deepcopy(candidate_a.getGenes())
                children_gene_b = copy.deepcopy(candidate_b.getGenes())

            children_genes.append(children_gene_a)
            children_genes.append(children_gene_b)
            # do mutation
            for child_genes in children_genes:
                self.DoMutation(child_genes)
                child_chromosome = Chromosome(child_genes)
                while not self.__is_child_acceptable(child_chromosome, offspring):
                    self.DoMutation(child_genes)
                    child_chromosome = Chromosome(child_genes)
                    # print("stuck")
                offspring.append(child_chromosome)


        return offspring

    def __is_child_acceptable(self, child, offspring):
        if child in self._pool or child in offspring:
            # print('existing')
            return False
        return True
    def CalculateStudentsFitness(self, pool, stu_list):
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
            # studentFitness = 65536 * selectedProjectsRank[0] \
            #                  + 256 * selectedProjectsRank[1] \
            #                  + 16 * selectedProjectsRank[2] + \
            #                  4 * selectedProjectsRank[3] \
            #                  + 2 * selectedProjectsRank[4]
            studentFitness = 25 * selectedProjectsRank[0] \
                             + 16 * selectedProjectsRank[1] \
                             + 9 * selectedProjectsRank[2] + \
                             4 * selectedProjectsRank[3] \
                             + 1 * selectedProjectsRank[4]
            individual.StudentsFitness = studentFitness + 1

    # @staticmethod

    def CalculateSupervisorsFitness(self, pool, proj_list, sup_list):
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
                        # if cur_stu_num <= quota / 2 + 1:
                        #     fitness_workload = fitness_workload + (cur_stu_num * 10) ^ 2
                        # else:
                        #     fitness_workload = fitness_workload + cur_stu_num
                        fitness_workload = fitness_workload + (quota - cur_stu_num) ^ 2
                        sup_preference_list = sup_list[sup].getProjectList()

                        for proj in selected_proj_list:
                            rank = sup_preference_list.index(proj)
                            fitness_satisfaction = fitness_satisfaction + (5 - rank) ^ 2
            individual.SupervisorsFitness = fitness_satisfaction + fitness_workload
            individual.SelectedSupervisorsAndProjects = selectedSupervisorsAndNum

    def DoMutation(self, child_genes):
        for i in range(len(child_genes)):
            rate = random.uniform(0, 1)
            # if rate < self._mutate_rate + random.uniform(0, 1-self._generation/self._max_generations):
            if rate < self._mutate_rate:
                child_genes = self.mutate(child_genes)

    def new_mutation(self, genes, i):
        genes = np.array(genes)
        point_1, point_2 = np.random.choice(len(genes), 2)
        start, end = min([point_1, point_2]), max([point_1, point_2])
        scrambled_order = np.random.choice(np.arange(start, end), end - start)
        genes[start:end] = genes[scrambled_order]

    def getBestIndividuals(self, pool):
        sorted_pool = sorted(pool, key=lambda x: x.Rank)
        ranks = []
        for k, g in groupby(sorted_pool, lambda x: x.Rank):
            ranks.append(list(g))
        return ranks[0]

    def mutate(self, genes):
        mutation_strategies = ['inversion', 'rotation', 'scramble', 'swap']
        mutation_strategy = random.choice(mutation_strategies)
        start, end = self._generate_two_points(len(genes))
        # return self.scramble_mutation(genes, start, end)
        if mutation_strategy is 'rotation':
            return self.rotation_mutation(genes, start, end)
        elif mutation_strategy is 'inversion':
            return self.inversion_mutation(genes, start, end)
        elif mutation_strategy is 'scramble':
            return self.scramble_mutation(genes, start, end)
        elif mutation_strategy is 'swap':
            return self.swap_mutation(genes, start, end)

    def swap_mutation(self, genes, start, end):
        genes[start], genes[end] = genes[end], genes[start]
        return genes

    def scramble_mutation(self, genes, start, end):
        genes = np.array(genes)
        scrambled_order = np.random.choice(np.arange(start, end), end - start)
        genes[start:end] = genes[scrambled_order]
        return genes.tolist()

    def rotation_mutation(self, genes, start, end):
        no_of_reverse = end - start + 1
        # By incrementing count value swapping
        # of first and last elements is done.
        count = 0
        while no_of_reverse // 2 != count:
            genes[start + count], genes[end - count] = genes[end - count], genes[start + count]
            count += 1
        return genes

    def inversion_mutation(self, genes, start, end):
        for i in range(start, (start + end) // 2 + 1):
            genes[i], genes[start + end - i] = genes[start + end - i], genes[i]
        return genes

    def _generate_two_points(self, len_genes):
        point_1, point_2 = np.random.choice(len_genes, 2)
        while point_1 == point_2:
            point_1, point_2 = np.random.choice(len_genes, 2)
        start, end = min([point_1, point_2]), max([point_1, point_2])
        return start, end

    def crossover_PMX(self, parentGenes, donorGenes, start, end):
        child_1 = np.array(copy.deepcopy(parentGenes))
        child_2 = np.array(copy.deepcopy(donorGenes))
        length = len(parentGenes)
        start_end_range = range(start, end)
        left = np.delete(range(length), start_end_range)

        left_parent, left_donor = child_1[left], child_2[left]
        cross_part_parent, cross_part_donor = child_1[start_end_range], child_2[start_end_range]

        child_1[start_end_range], child_2[start_end_range] = cross_part_donor, cross_part_parent

        mapping = [[], []]

        for i, j in zip(cross_part_parent, cross_part_donor):
            if j in cross_part_parent and i not in cross_part_donor:
                index = np.argwhere(cross_part_parent == j)[0, 0]
                value = cross_part_donor[index]
                while True:
                    if value in cross_part_parent:
                        index = np.argwhere(cross_part_parent == value)[0, 0]
                        value = cross_part_donor[index]
                    else:
                        break
                mapping[0].append(i)
                mapping[1].append(value)

            elif i in cross_part_donor:
                pass

            else:
                mapping[0].append(i)
                mapping[1].append(j)

        for i, j in zip(mapping[0], mapping[1]):
            if i in left_parent:
                left_parent[np.argwhere(left_parent == i)[0, 0]] = j
            elif i in left_donor:
                left_donor[np.argwhere(left_donor == i)[0, 0]] = j
            if j in left_parent:
                left_parent[np.argwhere(left_parent == j)[0, 0]] = i
            elif j in left_donor:
                left_donor[np.argwhere(left_donor == j)[0, 0]] = i

        child_1[left], child_2[left] = left_parent, left_donor
        return child_1.tolist()

    def get_candidates(self, pool):
        total_nums = len(pool) - 1
        index_1 = random.randint(0, total_nums)
        index_2 = random.randint(0, total_nums)
        while index_2 == index_1:
            index_2 = random.randint(0, total_nums)

        rival_1 = pool[index_1]
        rival_2 = pool[index_2]

        return rival_1, rival_2

    def tournamentSelection(self, rival_1, rival_2):
        if rival_1.Rank < rival_2.Rank:
            return rival_1
        elif rival_1.Rank == rival_2.Rank:
            if rival_1.CrowdingDistance > rival_2.CrowdingDistance:
                return rival_1
            else:
                return rival_2
        else:
            return rival_2

    def displayIndividuals(self, individuals):
        for i in individuals:
            print(i.getGenes())
            print('Rank', i.Rank)
            print('i', i.All_Project_Ranks)
            print(i.CrowdingDistance)
            sup = i.SelectedSupervisorsAndProjects
            num_list = []
            for projs in sup.values():
                num_list.append(len(projs))
            print('supervisors:', num_list)
            # selectedlist_supAndproj = i.SelectedSupervisorsAndProjects
            # for k, v in selectedlist_supAndproj.items():
            #     print('sup: ', k, ' num: ', len(v))
            # print(i.StudentsFitness)
            print('Supervisors:', i.SupervisorsFitness)
            print('Students:', i.StudentsFitness)
        print('---------------------------------------------')

