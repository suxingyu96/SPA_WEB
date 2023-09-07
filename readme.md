# A Genetic Algorithm for Student-Project Allocation (SPA) Problem 

An algorithm in python that allocates project to students and also considers students' preferences over projects, supervisors' capacity, workload and preferences
over projects using NSGA-II. This algorithm has the ability to find Pareto optimal solutions for decision makers to make trade-off.

This algorithm is integrated with an website. See details in 1. Using web to generate selections.

Otherwise, this algorithm can run independently by giving the data files' paths. (Check the details in 2. Using Algorithm as a stand alone by giving text file as input)

## 1. Using web to generate selections

This website is developed with Python and chooses SQLite as database. The website users input data to database, then this GA gets data from database and run.

### Installation
This tool needs Python 3.5 or above.
#### Install and create a virtual environment

```commandline
python3 -m venv env
source env/bin/activate
```

#### Clone project from Github and deploy
Dependencies can be found in requirements.txt
```commandline
$ git clone git@github.com:suxingyu96/SPA_WEB.git
$ cd SPA_WEB
$ pip install -r requirements.txt
```

#### Run the website locally
```commandline
python3 manage.py runserver
```
Go to http://127.0.0.1:8000 and check if the web is running or not.

## 2. Using Algorithm as a stand alone by giving text file as input

### Installation


This tool needs Python 3.5 or above, and relies on `NumPy`.

You can install this by cloning from the repository:

```commandline
$ git clone git@github.com:suxingyu96/2023_SPA_GA.git
$ cd 2023_SPA_GA
$ python3 setup.py install
```

### Documentation

This section contains the steps to execute this tool.

#### Data import

This tool includes a DataReader to import data in **.txt** or **.csv** format from local files.

The data of students should be stored as:

| student ID | project 1 | project 2 | project 3 | project 4 | project 5 |
| ---------- | --------: | --------: | --------: | --------: | --------: |

The data of supervisors should be stored as:

| supervisor ID | quota | project 1 | project 2 | project ... |
| ------------- | :---- | --------: | --------: | ----------: |

The data of projects should be stored as:

| project ID | supervisor ID |
| ---------- | :------------ |

Setting configuration in **src/Config.py**, an example is listed below.

```python
class Config:

    population_size = 500
    mutation_rate = 0.01
    crossover_rate = 0.5
    data_visualization = False


    students_file_path = str("path of students data")
    projects_file_path = str("path of projects data")
    supervisors_file_path = str("path of supervisors data")
```

#### Run the GA

After creating the lists of data, it is time to run the GA.

Executing the file in terminal:

```commandline
python3 main_run_GA.py
```
