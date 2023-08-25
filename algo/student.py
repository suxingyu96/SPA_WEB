class Student:

    def __init__(self, name, stuID, projectList: list, project_id=None):
        self.__name = name
        self.__stuID = stuID
        self.__projectList = projectList
        self.__project_id = None

    def getStudentName(self):
        return self.__name

    def getStudentID(self):
        return self.__stuID

    def getProjectList(self):
        return self.__projectList
    
    def __str__(self) -> str:
        return str(self.__stuID)
