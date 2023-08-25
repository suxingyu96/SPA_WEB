class Supervisor:

    def __init__(self, name, supID, projectList: list, quota: int):
        self.name = name
        self.supID = supID
        self.projectList = projectList
        self.quota = quota


    def getSupervisorName(self):
        return self.name

    def getSupervisorID(self):
        return self.supID

    def getProjectList(self):
        return self.projectList

    def getQuota(self):
        return self.quota
