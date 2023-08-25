import numpy as np
import matplotlib.pyplot as plt
from operator import attrgetter
from pygame import Vector2 as v2
class ParetoVisualScreen:

    def __init__(self):
        self.graphSize = v2(1000, 1000)
        plt.ion()
        self.ax = plt.gca()
        self.ax.set_autoscale_on(True)



    def Update(self, pool, generation):
        x_list = []
        y_list = []
        x_pareto = []
        y_pareto = []
        #  X axis
        minSupervisorsFitness = min(pool, key=attrgetter('NormalizedSupervisorsFitness'))\
            .NormalizedSupervisorsFitness
        maxSupervisorsFitness = max(pool, key=attrgetter('NormalizedSupervisorsFitness'))\
            .NormalizedSupervisorsFitness
        diffSupervisorsFitness = maxSupervisorsFitness - minSupervisorsFitness

        # Y axis
        minStudentsFitness = min(pool, key=attrgetter('NormalizedStudentsFitness')).NormalizedStudentsFitness
        maxStudentsFitness = max(pool, key=attrgetter('NormalizedStudentsFitness')).NormalizedStudentsFitness
        diffStudentsFitness = maxStudentsFitness - minStudentsFitness

        maxRank = max(pool, key=attrgetter('Rank')).Rank

        for i in range(len(pool)):
            individual = pool[i]
            if individual.Rank == 1:
                x = individual.SupervisorsFitness
                y = individual.StudentsFitness
                x_pareto.append(x)
                y_pareto.append(y)
                continue

            x = individual.SupervisorsFitness
            y = individual.StudentsFitness
            # x = (individual.NormalizedSupervisorsFitness - minSupervisorsFitness)\
            #     /diffSupervisorsFitness * self.graphSize.x
            # y = (individual.NormalizedStudentsFitness - minStudentsFitness)/diffStudentsFitness * self.graphSize.y

            x_list.append(x)
            y_list.append(y)

        pos_pareto_x = np.array(x_pareto)
        pos_pareto_y = np.array(y_pareto)
        positions_x = np.array(x_list)
        positions_y = np.array(y_list)

        lines, = self.ax.plot([], [], 'o')
        pareto_line, = self.ax.plot([], [], '*', color="red")
        pareto_line.set_xdata(pos_pareto_x)
        pareto_line.set_ydata(pos_pareto_y)
        lines.set_xdata(positions_x)
        lines.set_ydata(positions_y)

        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
        #We need to draw *and* flush
        # self.figure.canvas.draw()
        # self.figure.canvas.flush_events()
        plt.text(900, 60, generation, fontsize = 22)
        plt.draw()
        plt.pause(0.1)
        plt.cla()



    # def clear(self):
        # self.window.cla()
#
# pareto = ParetoVisualScreen(1)
# pareto.showWindow()
