import copy
import random
import statistics
import sys
import time

import numpy as np
from itertools import groupby
from algo.MultiObjectiveHelper import MultiObjectiveHelper
from algo.Chromosome import Chromosome
from algo.ParetoVisualScreen import ParetoVisualScreen
from algo.Slice import Slice


class SPA_genetic_algorithm:
    def __init__(self, stu_list, proj_list, sup_list):
        self._numParents = 3
        self._mutate_rate = 0.4
        self._stu_list = stu_list
        self._proj_list = proj_list
        self._sup_list = sup_list
        self._geneSet = self.__create_geneset()
        self._pool = self.__generate_first_population()


    def __generate_first_population(self):
        lenOfgenes = len(self._stu_list)
        pool = [self.generate_parent(self._geneSet, lenOfgenes) for _ in range(self._numParents)]

        for i in range(len(pool)):
            genes = pool[i]
            individual = Chromosome(genes)
            pool[i] = individual
        return pool

    def run(self, max_generations=100, max_noImprovementCount=80):
        generation = 0
        print('generation', generation)
        self._pool = MultiObjectiveHelper.UpdatePopulationFitness(self._pool, self._stu_list, self._proj_list, self._sup_list)
        # paretoFrontWindow = ParetoVisualScreen()
        # Termination Condition
        isConverged = False
        NoImprovementCount = 0
        preConvergenceArea = 0
        while not isConverged:
            # paretoFrontWindow.Update(pool, generation)
            # time.sleep(1)

            bestIndividuals = self.getBestIndividuals(self._pool)
            sorted_bestIndividuals = sorted(bestIndividuals, key=lambda x: (x.Rank, x.SupervisorsFitness))
            curArea = MultiObjectiveHelper.CalculateArea(sorted_bestIndividuals)
            if abs(curArea - preConvergenceArea) < 0.05 * preConvergenceArea:
                NoImprovementCount += 1
            else:
                NoImprovementCount = 0
                preConvergenceArea = curArea

            print("{0} number: {1}".format(generation, len(self._pool)))
            print('The bests:', len(bestIndividuals))
            for i in bestIndividuals:
                print('solution:')
                print(i.getGenes())
                print('Rank', i.Rank)
                print('i', i.All_Project_Ranks)
                print(i.CrowdingDistance)
                sup = i.SelectedSupervisorsAndProjects
                num_list = []
                if len(sup)!=0:
                    for projs in sup.values():
                        num_list.append(len(projs))
                print('supervisors:', num_list)
                # selectedlist_supAndproj = i.SelectedSupervisorsAndProjects
                # for k, v in selectedlist_supAndproj.items():
                #     print('sup: ', k, ' num: ', len(v))
                # print(i.StudentsFitness)
                print(i.SupervisorsFitness)

            print('---------------------------------------------')

            generation += 1

            offspring = self.generateOffspring(self._pool, self._mutate_rate, self._geneSet)
            self._pool.extend(offspring)
            self._pool = MultiObjectiveHelper.UpdatePopulationFitness(self._pool,
                                                                      self._stu_list,
                                                                      self._proj_list,
                                                                      self._sup_list)

            newPopulation = []
            sorted_pool = sorted(self._pool, key=lambda x: (x.Rank, 0 - x.CrowdingDistance))
            for i in sorted_pool:
                if i not in newPopulation:
                    newPopulation.append(i)
                if len(newPopulation) >= 0.9 * self._numParents:
                    break

            while len(newPopulation) < self._numParents:
                randomIndividual = random.choice(sorted_pool)
                if randomIndividual not in newPopulation:
                    newPopulation.append(randomIndividual)

            self._pool.clear()
            self._pool = newPopulation
            isConverged = generation >= max_generations or NoImprovementCount > max_noImprovementCount
        return bestIndividuals

    def __create_geneset(self):
        geneSet = []
        for id, project in self._proj_list.items():
            project_id = id
            geneSet.append(project_id)

        return geneSet

    def generate_parent(self, geneSet, lenOfGenes):
        return random.sample(geneSet, lenOfGenes)

    def generateOffspring(self, pool, mutate_rate, geneSet):
        offspring = []
        print('num of pool', len(pool))
        print('mutation rate:', mutate_rate)
        while len(offspring) < len(pool):
            # crossover
            parent = self.tournamentSelection(pool)
            donor = self.tournamentSelection(pool)
            while parent == donor:
                donor = self.tournamentSelection(pool)
            child_genes = self.crossover_PMX(parent.getGenes(), donor.getGenes())

            # do mutation
            rate = random.uniform(0, 1)
            if rate < mutate_rate:
                self.mutate(child_genes)

            # while child gene exists
            child_chromosome = Chromosome(child_genes)
            while child_chromosome in pool \
                    or child_chromosome == parent or child_chromosome == donor:
                lenOfGenes = len(child_genes)
                child_genes = self.generate_parent(geneSet, lenOfGenes)
                child_chromosome = Chromosome(child_genes)

            offspring.append(child_chromosome)
        return offspring

    def getBestIndividuals(self, pool):
        sorted_pool = sorted(pool, key=lambda x: x.Rank)
        ranks = []
        for k, g in groupby(sorted_pool, lambda x: x.Rank):
            ranks.append(list(g))
        return ranks[0]

    def mutate(self, genes):
        mutation_strategies = ['inversion', 'rotation', 'scramble']
        mutation_strategy = random.choice(mutation_strategies)
        if mutation_strategy == 'rotation':
            self.rotation_mutation(genes)
        elif mutation_strategy == 'inversion':
            self.inversion_mutation(genes)
        elif mutation_strategy == 'scramble':
            self.scramble_mutation(genes)

    def scramble_mutation(self, genes):
        genes = np.array(genes)
        point_1, point_2 = np.random.choice(len(genes), 2)
        start, end = min([point_1, point_2]), max([point_1, point_2])
        scrambled_order = np.random.choice(np.arange(start, end), end - start)
        genes[start:end] = genes[scrambled_order]

    def rotation_mutation(self, genes):
        point_1, point_2 = np.random.choice(len(genes), 2)
        start, end = min([point_1, point_2]), max([point_1, point_2])

        no_of_reverse = end - start + 1
        # By incrementing count value swapping
        # of first and last elements is done.
        count = 0
        while no_of_reverse // 2 != count:
            genes[start + count], genes[end - count] = genes[end - count], genes[start + count]
            count += 1

    def inversion_mutation(self, genes):
        point_1, point_2 = np.random.choice(len(genes), 2)
        start, end = min([point_1, point_2]), max([point_1, point_2])
        for i in range(start, (start + end) // 2 + 1):
            genes[i], genes[start + end - i] = genes[start + end - i], genes[i]

    def crossover_PMX(self, parentGenes, donorGenes):
        child_1 = np.array(copy.deepcopy(parentGenes))
        child_2 = np.array(copy.deepcopy(donorGenes))
        length = len(parentGenes)
        point_1, point_2 = np.random.choice(length, 2)
        start, end = min([point_1, point_2]), max([point_1, point_2])
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
        # return child_1.tolist()
        return child_1.tolist()

    def tournamentSelection(self, pool):
        total_nums = len(pool) - 1
        pool = np.asarray(pool)
        index_1 = random.randint(0, total_nums)
        index_2 = random.randint(0, total_nums)
        while index_2 == index_1:
            index_2 = random.randint(0, total_nums)

        rival_1 = pool[index_1]
        rival_2 = pool[index_2]
        if rival_1.Rank < rival_2.Rank:
            return rival_1
        elif rival_1.Rank == rival_2.Rank:
            if rival_1.CrowdingDistance > rival_2.CrowdingDistance:
                return rival_1
            else:
                return rival_2
        else:
            return rival_2


class Benchmark:
    @staticmethod
    def run(function, stu_list, sup_list, proj_list):
        timings = []
        stdout = sys.stdout
        # run 3 times and check the average performance and deviation
        for i in range(3):
            sys.stdout = NullWriter()
            startTime = time.time()
            function(stu_list, sup_list, proj_list)
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{0} {1:3.2f} {2:3.2f}".format(1 + i, mean,
                                                     statistics.stdev(timings, mean) if i > 1 else 0))


class NullWriter():
    def getvalue(self):
        pass

    def write(self, s):
        pass
