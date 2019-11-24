from PyQt5 import  QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget, QGridLayout, QMainWindow, QLineEdit, QPushButton, QComboBox


import os
import numpy as np
from numpy import cos
from matplotlib.figure import Figure # For Matplotlib Figure Object
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from Option3d import *
import sys
from matplotlib import cm


class ThreeDSurface_GraphWindow(FigureCanvas): #Class for 3D window
    def __init__(self):
        self.fig =plt.figure(figsize=(7,7))
        FigureCanvas.__init__(self, self.fig) #creating FigureCanvas
        self.axes = self.fig.gca(projection='3d')#generates 3D Axes object
        self.setWindowTitle("Main") # sets Window title

    def DrawGraph(self, x, y, z, z_label, title):#Fun for Graph plotting
        self.axes.clear()
        self.axes.set_zlabel(z_label)
        self.axes.set_ylabel('Spot')
        self.axes.set_xlabel('DTE')
        self.fig.suptitle(title)
        self.axes.plot_surface(x, y, z, cmap = cm.coolwarm) #plots the 3D surface plot
        self.draw()


#### PyQt5 GUI ####
class MainWindow(QWidget):
    def __init__(self, parent = None):

        super(MainWindow,self).__init__()

    ## GRID LAYOUT
        self.layout = QGridLayout()
        self.input_layout = QGridLayout()

        
        self.ThreeDWin = ThreeDSurface_GraphWindow()
        self.layout.addWidget(self.ThreeDWin, 2, 0, 1, 4)

        self.strike_input_label = QLabel(self)
        self.strike_input_label.setText("Strike: ")
        self.strike_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.strike_input_label, 0, 0)
        self.strike_input = QLineEdit(self)
        self.input_layout.addWidget(self.strike_input, 0, 1)

        self.spot_input_label = QLabel(self)
        self.spot_input_label.setText("Spot: ")
        self.spot_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.spot_input_label, 0, 2)
        self.spot_input = QLineEdit(self)
        self.input_layout.addWidget(self.spot_input, 0, 3)

        self.exp_input_label = QLabel(self)
        self.exp_input_label.setText("DTE: ")
        self.exp_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.exp_input_label, 0, 4)
        self.exp_input = QLineEdit(self)
        self.input_layout.addWidget(self.exp_input, 0, 5)

        self.iv_input_label = QLabel(self)
        self.iv_input_label.setText("IV: ")
        self.iv_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.iv_input_label, 0, 6)
        self.iv_input = QLineEdit(self)
        self.input_layout.addWidget(self.iv_input, 0, 7)

        self.r_input_label = QLabel(self)
        self.r_input_label.setText("R: ")
        self.r_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.r_input_label, 0, 8)
        self.r_input = QLineEdit(self)
        self.input_layout.addWidget(self.r_input, 0, 9)

        self.sw_input_label = QLabel(self)
        self.sw_input_label.setText("Spot Width: ")
        self.sw_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.sw_input_label, 1, 0)
        self.sw_input = QLineEdit(self)
        self.input_layout.addWidget(self.sw_input, 1, 1)


        self.ss_input_label = QLabel(self)
        self.ss_input_label.setText("Spot Step: ")
        self.ss_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ss_input_label, 1, 2)
        self.ss_input = QLineEdit(self)
        self.input_layout.addWidget(self.ss_input, 1, 3)

        self.ts_input_label = QLabel(self)
        self.ts_input_label.setText("Time Step: ")
        self.ts_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ts_input_label, 1, 4)
        self.ts_input = QLineEdit(self)
        self.input_layout.addWidget(self.ts_input, 1, 5)

        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("P/L")
        self.comboBox.addItem("Delta")
        self.comboBox.addItem("Gamma")
        self.comboBox.addItem("Theta")
        self.comboBox.addItem("Vega")
        self.input_layout.addWidget(self.comboBox, 1, 6)

        self.button = QPushButton('Submit', self)
        self.input_layout.addWidget(self.button, 1, 7)
        self.button.clicked.connect(self.init_plot)
      
        self.layout.addLayout(self.input_layout, 0, 0, 1, 4)
        
        self.setLayout(self.layout)

        
    def init_plot(self, MainWindow):

        try:

            self.strike = float(self.strike_input.text())
            self.spot = float(self.spot_input.text())
            self.iv = float(self.iv_input.text())
            self.r = float(self.r_input.text())
            self.ss = float(self.ss_input.text())
            self.sw = float(self.sw_input.text())
            self.ts = float(self.ts_input.text())
            self.exp = float(self.exp_input.text())

        except:
            print("Failed to gather inputs")

        target = str(self.comboBox.currentText())

        self.array = np.array(
        [[1, 0, self.spot, self.strike, self.exp, self.iv, self.sw, self.ss, self.ts]],
        np.float64
            )

        
        self.df = main_array(self.array, target)
        self.x = self.df.columns.values
        self.y = self.df.index.values
        Z = self.df.values
        
        X,Y=np.meshgrid(self.x,self.y)

        title = target + " for " + str(self.strike) + " " + "Call with " + str(self.iv*100) + "% IV" + " and " + str(self.exp) + " DTE"
        self.ThreeDWin.DrawGraph(X, Y, Z, target, title)
            
        
if __name__ == "__main__":
        App = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(App.exec())
