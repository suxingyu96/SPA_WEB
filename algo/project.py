# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# file_handler = logging.FileHandler('../logs/projects.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)
class Project:
    def __init__(self, projectID, supervisor_id):
        self.projectID = projectID
        # self.student = student
        self.supervisor_id = supervisor_id


    def getSupervisor(self):
        return self.supervisor_id
