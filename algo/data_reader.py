from project import Project
from student import Student
from supervisor import Supervisor
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('../logs/data_reader.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class DataReader:

    def __init__(self, sup_list_path, stu_list_path, proj_list_path):
        self.__sup_list_path = sup_list_path
        self.__stu_list_path = stu_list_path
        self.__proj_list_path = proj_list_path

        self.__sup_list = self.__generate_supervisor_list()
        self.__proj_list = self.__generate_project_list()
        self.__stu_list = self.__generate_stu_list()

    def getStudentList(self):
        return self.__stu_list

    def getSupervisorList(self):
        return self.__sup_list

    def getProjectList(self):
        return self.__proj_list

    def __generate_stu_list(self):
        logger.info("Reading students\' data from the given path: {0} ".format(self.__stu_list_path))
        # logger.info(str('Reading students\' data from the given path: ' + self.__stu_list_path))
        stu_file = open(self.__stu_list_path, "r")
        stu_list = []
        for stu in stu_file:
            stu_info = stu.split()
            stu_id = int(stu_info[0])
            stu_preferences_list = []
            for item in stu_info[1:]:
                stu_preferences_list.append(int(item))
            student = Student(stu_id, stu_id, stu_preferences_list)
            if self.__student_constraints_check(student, self.__proj_list):
                stu_list.append(student)
        stu_file.close()
        logger.info('Get students\' data successfully')
        return stu_list

    def __generate_supervisor_list(self):
        logger.info("Reading supervisors\' data from the given path: {0} ".format(self.__sup_list_path))
        sup_file = open(self.__sup_list_path, "r")
        sup_list = []
        for sup in sup_file:
            sup_info = sup.split()
            sup_id = int(sup_info[0])
            sup_quota = int(sup_info[1])
            sup_proj_list = []
            for item in sup_info[2:]:
                sup_proj_list.append(int(item))
            supervisor = Supervisor(sup_id, sup_id, sup_proj_list, sup_quota)
            sup_list.append(supervisor)
        sup_file.close()
        logger.info('Get supervisors\' data successfully')
        return sup_list

    def __generate_project_list(self):
        logger.info("Reading projects\' data from the given path: {0} ".format(self.__proj_list_path))
        proj_file = open(self.__proj_list_path, "r")
        proj_list = []
        for proj in proj_file:
            logger.info('project id:')
            logger.info(proj)
            proj_info = proj.split()
            proj_id = int(proj_info[0])
            proj_sup = int(proj_info[1])
            project = Project(proj_id, proj_sup)
            proj_list.append(project)
        proj_file.close()
        logger.info('Get projects\' data successfully')
        return proj_list

    def __student_constraints_check(self, stu: Student, proj_list: list):
        preference_list = stu.getProjectList()
        sup_set = set()
        for proj in preference_list:
            sup_id = proj_list[proj].supervisor_id
            sup_set.add(sup_id)
        if (len(sup_set)) > 1:
            return True
        logger.error("Student id: {0} only choose one supervisor, please choose at least two supervisors"
                     .format(stu.getStudentID()))
        return False
