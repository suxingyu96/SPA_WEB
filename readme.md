# A Genetic Algorithm for Student-Project Allocation (SPA) Problem
An algorithm in python that allocate project to students and also considers students' preferences over projects, supervisors' capacity, workload and preferences 
over projects using NSGA-II. This algorithm has the ability to find optimal solutions for decision makers to make trade-off.

## Installation
This tool needs Python 3.5 or above, and relies on `NumPy`.

You can install this by cloning from the repository:
```git 
$ git clone git@github.com:suxingyu96/2023_SPA_GA.git
$ cd 2023_SPA_GA
$ python3 setup.py install
```
## Documentation 
This section contains the steps to execute this tool.

### Data import

This tool includes a DataReader to import data in **.txt** or **.csv** format from local files.

The data of students should be stored as:

| student ID | project 1  |  project 2 |  project 3 |project 4 | project 5 |
|------------|-----------:|-----------:|-----------:|---------:|----------:|


The data of supervisors should be stored as:

| supervisor ID | quota |project 1 | project 2 | project ... |
|-------|:----------|----------:|------------:|---------:|

The data of projects should be stored as:

| project ID | supervisor ID |
|-------|:----------|



Setting configuration in **src/Config.py**, an example is listed below. 
```python
class Config:

    population_size = 500
    mutation_rate = 1/(population_size * 7)
    crossover_rate = 0.5
    data_visualization = False


    students_file_path = str("path of students data")
    projects_file_path = str("path of projects data")
    supervisors_file_path = str("path of supervisors data")
```

### Run the GA
After creating the lists of data, it is time to run the GA. 

Executing the file in terminal:
```commandline
python3 main_run_GA.py
```
