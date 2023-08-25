import random
import copy


class Chromosome:
    _genes = None
    _fitness = None
    Rank = None
    CrowdingDistance = None
    StudentsFitness = None
    All_Project_Ranks = None
    SelectedSupervisorsAndProjects = {}
    SupervisorsFitness = None
    NormalizedStudentsFitness = None
    NormalizedSupervisorsFitness = None

    def __init__(self, genes):
        self._genes = genes
        # self._fitness = fitness

    def getGenes(self):
        return self._genes

    def getFitness(self):
        return self._fitness

    def __eq__(self, obj):
        return self._genes == obj.getGenes()

    def __str__(self):
        return str(self.All_Project_Ranks)
    
    

