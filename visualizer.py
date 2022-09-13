#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg
import math
from datetime import datetime

pg.setConfigOption('foreground', 'y') # Sets the axes and grid to yellow to have some distinction between the UI and the plotted values.


class Visualization(QtWidgets.QWidget):
    """Extends PyQT5's QWidget. This class creates an object that visualizes a given function in a GUI.
    """
    def __init__(self):
        """_Initializes the visualization class including its methods, important variables and the timer needed for iterative updates of the GUI.
        """
        super(Visualization, self).__init__()
        self.init_ui()
        self.qt_connections()
        self.plot_curve = pg.PlotCurveItem()
        self.plot_widget.addItem(self.plot_curve)
        self.t = 0
        self.update_rate = 10  # in ms
        self.time_interval = self.update_rate / 1000
        self.data_array = []
        self.time_array = []
        self.active = True
        self.update_plot()

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(lambda:self.update_plot())
        self.timer.start(self.update_rate)

    def init_ui(self):
        """Initialization of the GUI.
        """
        hbox = QtWidgets.QVBoxLayout()
        self.setLayout(hbox)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(x=True, y=True, alpha=0.4)
        hbox.addWidget(self.plot_widget)

        self.startbutton = QtWidgets.QPushButton("Start")
        self.stopbutton = QtWidgets.QPushButton("Stop")
        self.resetbutton = QtWidgets.QPushButton("Reset")
        self.nameLabel = QtWidgets.QLabel(self)
        self.nameLabel.setText('Experiment name:')
        self.line = QtWidgets.QLineEdit(self)
        self.savebutton = QtWidgets.QPushButton("Save data as .csv")
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setWindowTitle("Error")
        self.error_dialog.setText("Error: experiment name cannot be empty!")

        hbox.addWidget(self.startbutton)
        hbox.addWidget(self.stopbutton)
        hbox.addWidget(self.resetbutton)
        hbox.addWidget(self.nameLabel)
        hbox.addWidget(self.line)
        hbox.addWidget(self.savebutton)

        self.setGeometry(10, 10, 2000, 1200)
        self.setWindowTitle('KTH Formula Student Visualization Exercise')
        self.show()

    def on_startbutton_clicked(self):
        """Sets self.active to True in order to allow the iterative function calculation in the method 'calculate_function'.
        """
        self.active = True

    def on_stopbutton_clicked(self):
        """Sets self.active to False in order to stop the iterative function calculation in the method 'calculate_function'.
        """
        self.active = False

    def on_resetbutton_clicked(self):
        """Empties the stored data entries in self.data_array and resets self.t to zero.
        """
        self.data_array
        self.t = 0.0
        self.plot_curve.setData(self.data_array)

    def on_savebutton_clicked(self):
        """Save the data currently stored in self.data_array into a .csv file along with its t value.
        """
        experimentName = self.line.text()

        if experimentName != "":
            saveName = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + \
                "_" + experimentName + ".csv"
            np.savetxt(saveName, np.c_[np.array(self.time_array),
                       np.array(self.data_array)], delimiter=',')
        else:
            x = self.error_dialog.exec_()

    def calculate_function(self, t):
        """A method that calculates the function h(t) = 3*pi*exp(-lambda[t]) with where lambda(t) = 5*sin(2*pi*1*t).

        Args:
            t (Float): Input, in this case time to, to calculate h(t)

        Returns:
            Float: The result of the function h(t)(described above)
        """
        _lambda = 5 * math.sin(2 * math.pi * 1 * t)
        h_t = 3 * math.pi * math.exp(-_lambda)
        return h_t

    def update_plot(self):
        """If data generation is not paused, t gets incremented by the set time interval andafter that, the function of interest is calculated and added to the plotcurve element.
        """
        if self.active:
            var = self.calculate_function(self.t)
            self.data_array.append(var)
            self.time_array.append(self.t)
            self.plot_curve.setData(self.time_array, self.data_array)
            self.t += self.time_interval
            self.t = round(self.t, 2)

    def qt_connections(self):
        """Connects the GUI's buttons with the corresponding onClick methods.
        """
        self.startbutton.clicked.connect(self.on_startbutton_clicked)
        self.stopbutton.clicked.connect(self.on_stopbutton_clicked)
        self.resetbutton.clicked.connect(self.on_resetbutton_clicked)
        self.savebutton.clicked.connect(self.on_savebutton_clicked)


def main():
    """Starts the visualization application by generating a new Visualization object
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('KTH Visualization Exercise')
    ex = Visualization()

    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
