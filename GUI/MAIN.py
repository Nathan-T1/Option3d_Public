from PyQt5 import  QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget, QGridLayout, QMainWindow, QLineEdit, QPushButton, QComboBox


import os
import numpy as np
from matplotlib.figure import Figure # For Matplotlib Figure Object
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from Option3d import *
import sys
from matplotlib import cm
import pandas as pd 


class ThreeDSurface_GraphWindow(FigureCanvas): #Class for 3D window
    def __init__(self):
        self.fig =plt.figure(figsize=(7,7))
        FigureCanvas.__init__(self, self.fig) #creating FigureCanvas
        self.axes = self.fig.gca(projection='3d')#generates 3D Axes object
        self.setWindowTitle("Main") # sets Window title

    def DrawGraph(self, x, y, z, z_label):
        self.axes.clear()
        self.axes.set_zlabel(z_label)
        self.axes.set_ylabel('Spot')
        self.axes.set_xlabel('DTE')
        #self.fig.suptitle(title)
        self.axes.plot_surface(x, y, z, cmap = cm.coolwarm) #plots the 3D surface plot
        self.draw()
    


#### PyQt5 GUI ####
class MainWindow_single(QWidget):
    def __init__(self, parent = None):

        super(MainWindow_single,self).__init__()

    ## GRID LAYOUT
        self.layout = QGridLayout()
        self.input_frame = QtWidgets.QFrame()
        self.input_layout = QGridLayout()

        
        self.ThreeDWin = ThreeDSurface_GraphWindow()
        self.layout.addWidget(self.ThreeDWin, 2, 0, 1, 4)

        self.layout_button = QPushButton('Toggle Inputs', self)
        self.layout.addWidget(self.layout_button, 3, 0)
        self.layout_button.clicked.connect(self.toggle_inputs)

        self.export_df_button = QPushButton('Export CSV', self)
        self.layout.addWidget(self.export_df_button, 3, 1)
        self.export_df_button.clicked.connect(self.export_df)

        self.export_df_button = QPushButton('Export PNG', self)
        self.layout.addWidget(self.export_df_button, 3, 2)
        self.export_df_button.clicked.connect(self.export_jpg)

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

        self.longshort_comboBox = QComboBox(self)
        self.longshort_comboBox.setObjectName(("comboBox"))
        self.longshort_comboBox.addItem("Long")
        self.longshort_comboBox.addItem("Short")
        self.input_layout.addWidget(self.longshort_comboBox, 1, 6)

        self.putcall_comboBox = QComboBox(self)
        self.putcall_comboBox.setObjectName(("comboBox"))
        self.putcall_comboBox.addItem("Put")
        self.putcall_comboBox.addItem("Call")
        self.input_layout.addWidget(self.putcall_comboBox, 1, 7)

        self.target_label = QLabel(self)
        self.target_label.setText("Target: ")
        self.target_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.target_label, 1, 8)
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("P/L")
        self.comboBox.addItem("Delta")
        self.comboBox.addItem("Gamma")
        self.comboBox.addItem("Theta")
        self.comboBox.addItem("Vega")
        self.input_layout.addWidget(self.comboBox, 1, 9)

        self.button = QPushButton('Submit', self)
        self.input_layout.addWidget(self.button, 2, 1)
        self.button.clicked.connect(self.init_plot)

        self.input_frame.setLayout(self.input_layout)
      
        self.layout.addWidget(self.input_frame, 0, 0, 1, 4)
        
        self.setLayout(self.layout)

    def toggle_inputs(self, MainWindow_single):

        self.input_frame.setHidden(not self.input_frame.isHidden())

    def export_jpg(self, MainWindow_single):

        
        self.ThreeDWin.fig.savefig('Option3d_fig.png', dpi = self.ThreeDWin.fig.dpi)
      

    def export_df(self, MainWindow_single_single):

        try:
            self.df.to_csv("Option3d_data.csv")
        except:
            print("No data to return")

        
    def init_plot(self, MainWindow_single):

        try:

            self.strike = float(self.strike_input.text())
            self.spot = float(self.spot_input.text())
            self.iv = float(self.iv_input.text())
            self.r = float(self.r_input.text())
            self.ss = float(self.ss_input.text())
            self.sw = float(self.sw_input.text())
            self.ts = float(self.ts_input.text())
            self.exp = float(self.exp_input.text())
            
            self.target = str(self.comboBox.currentText())
            self.longshort = str(self.longshort_comboBox.currentText())
            self.putcall = str(self.putcall_comboBox.currentText())

        except:
            print("Failed to gather inputs")

        if self.longshort == 'Long':
            self.scaler = 1
        else:
            self.scaler = -1
        if self.putcall == 'Put':
            self.type = 1
        else:
            self.type = 0

        self.array = np.array(
        [[self.scaler, self.type, self.spot, self.strike, self.exp, self.iv, self.sw, self.ss, self.ts]],
        np.float64
            )

        self.df = main_array(self.array, self.target)
        self.x = self.df.columns.values
        self.y = self.df.index.values
        Z = self.df.values
        
        X,Y=np.meshgrid(self.x,self.y)

        #title = self.target + " for " + str(self.strike) + " " + "Call with " + str(self.iv*100) + "% IV" + " and " + str(self.exp) + " DTE"
        self.ThreeDWin.DrawGraph(X, Y, Z, self.target)

#### PyQt5 GUI ####
class MainWindow_double(QWidget):
    def __init__(self, parent = None):

        super(MainWindow_double,self).__init__()

    ## GRID LAYOUT
        self.layout = QGridLayout()
        self.input_frame = QtWidgets.QFrame()
        self.input_layout = QGridLayout()

        
        self.ThreeDWin = ThreeDSurface_GraphWindow()
        self.layout.addWidget(self.ThreeDWin, 2, 0, 1, 4)

        self.layout_button = QPushButton('Toggle Inputs', self)
        self.layout.addWidget(self.layout_button, 3, 0)
        self.layout_button.clicked.connect(self.toggle_inputs)

        self.export_df_button = QPushButton('Export CSV', self)
        self.layout.addWidget(self.export_df_button, 3, 1)
        self.export_df_button.clicked.connect(self.export_df)

        self.export_df_button = QPushButton('Export PNG', self)
        self.layout.addWidget(self.export_df_button, 3, 2)
        self.export_df_button.clicked.connect(self.export_jpg)

        my_range = [0,2]

        counter = 1
        for i in my_range:

            self.contract_label = QLabel(self)
            self.contract_label.setText("Contract {}:".format(counter))
            self.input_layout.addWidget(self.contract_label, i, 0)
            counter += 1
            
            self.strike_input_label = QLabel(self)
            self.strike_input_label.setText("Strike: ")
            self.strike_input_label.setStyleSheet('color: black')
            self.input_layout.addWidget(self.strike_input_label, i, 1)
            self.strike_input = QLineEdit(self)
            objname = "strike_{}".format(str(i))
            self.strike_input.setObjectName(objname)
            self.input_layout.addWidget(self.strike_input, i, 2)

            if i == 0:
                self.spot_input_label = QLabel(self)
                self.spot_input_label.setText("Spot: ")
                self.spot_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.spot_input_label, i, 3)
                self.spot_input = QLineEdit(self)
                objname = "spot_{}".format(str(i))
                self.spot_input.setObjectName(objname)
                self.input_layout.addWidget(self.spot_input, i, 4)
            if i == 0:
                self.exp_input_label = QLabel(self)
                self.exp_input_label.setText("DTE: ")
                self.exp_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.exp_input_label, i, 5)
                self.exp_input = QLineEdit(self)
                objname = "exp_{}".format(str(i))
                self.exp_input.setObjectName(objname)
                self.input_layout.addWidget(self.exp_input, i, 6)

            self.iv_input_label = QLabel(self)
            self.iv_input_label.setText("IV: ")
            self.iv_input_label.setStyleSheet('color: black')
            self.input_layout.addWidget(self.iv_input_label, i, 7)
            self.iv_input = QLineEdit(self)
            objname = "iv_{}".format(str(i))
            self.iv_input.setObjectName(objname)
            self.input_layout.addWidget(self.iv_input, i, 8)

            if i == 0:
                
                self.r_input_label = QLabel(self)
                self.r_input_label.setText("R: ")
                self.r_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.r_input_label, i, 9)
                self.r_input = QLineEdit(self)
                objname = "r_{}".format(str(i))
                self.r_input.setObjectName(objname)
                self.input_layout.addWidget(self.r_input, i, 10)

            self.longshort_comboBox = QComboBox(self)
            self.longshort_comboBox.setObjectName(("comboBox"))
            self.longshort_comboBox.addItem("Long")
            self.longshort_comboBox.addItem("Short")
            objname = "longshort_{}".format(str(i))
            self.longshort_comboBox.setObjectName(objname)
            self.input_layout.addWidget(self.longshort_comboBox, i + 1, 1)

            self.putcall_comboBox = QComboBox(self)
            self.putcall_comboBox.setObjectName(("comboBox"))
            self.putcall_comboBox.addItem("Put")
            self.putcall_comboBox.addItem("Call")
            objname = "putcall_{}".format(str(i))
            self.putcall_comboBox.setObjectName(objname)
            self.input_layout.addWidget(self.putcall_comboBox, i + 1, 2)

        self.contract_label = QLabel(self)
        self.contract_label.setText("Parameters: ")
        self.input_layout.addWidget(self.contract_label, 6, 0)
            
        self.sw_input_label = QLabel(self)
        self.sw_input_label.setText("Spot Width: ")
        self.sw_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.sw_input_label, 6, 1)
        self.sw_input = QLineEdit(self)
        self.input_layout.addWidget(self.sw_input, 6, 2)


        self.ss_input_label = QLabel(self)
        self.ss_input_label.setText("Spot Step: ")
        self.ss_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ss_input_label, 6, 3)
        self.ss_input = QLineEdit(self)
        self.input_layout.addWidget(self.ss_input, 6, 4)

        self.ts_input_label = QLabel(self)
        self.ts_input_label.setText("Time Step: ")
        self.ts_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ts_input_label, 6, 5)
        self.ts_input = QLineEdit(self)
        self.input_layout.addWidget(self.ts_input, 6, 6)

        self.target_label = QLabel(self)
        self.target_label.setText("Target: ")
        self.target_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.target_label, 6, 7)
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("P/L")
        self.comboBox.addItem("Delta")
        self.comboBox.addItem("Gamma")
        self.comboBox.addItem("Theta")
        self.comboBox.addItem("Vega")
        self.input_layout.addWidget(self.comboBox, 6, 8)

        self.button = QPushButton('Submit', self)
        self.input_layout.addWidget(self.button, 6, 10)
        self.button.clicked.connect(self.init_plot)

        self.input_frame.setLayout(self.input_layout)
        self.layout.addWidget(self.input_frame, 0, 0, 1, 4)
        self.setLayout(self.layout)

    def toggle_inputs(self, MainWindow_double):

        self.input_frame.setHidden(not self.input_frame.isHidden())

    def export_jpg(self, MainWindow_double):

        
        self.ThreeDWin.fig.savefig('Option3d_fig.png', dpi = self.ThreeDWin.fig.dpi)
      

    def export_df(self, MainWindow_double):

        try:
            self.df.to_csv("Option3d_data.csv")
        except:
            print("No data to return")

    def init_plot(self, MainWindow_double):

        my_range = ["0","2"]

        self.ss = float(self.ss_input.text())
        self.sw = float(self.sw_input.text())
        self.ts = float(self.ts_input.text())
        self.exp = float(self.exp_input.text())
        self.r = float(self.r_input.text())
        self.spot = float(self.spot_input.text())
        self.target = str(self.comboBox.currentText())

        self.main_array = np.zeros(shape=(2,9))
        counter = 0
        for i in my_range:
                
            self.strike = float(self.findChild(QtWidgets.QLineEdit, "strike_{}".format(i)).text())
            self.iv = float(self.findChild(QtWidgets.QLineEdit, "iv_{}".format(i)).text())
            self.putcall = str(self.findChild(QtWidgets.QComboBox, "putcall_{}".format(i)).currentText())
            self.longshort = str(self.findChild(QtWidgets.QComboBox, "longshort_{}".format(i)).currentText())

            if self.longshort == 'Long':
                self.scaler = 1
            else:
                self.scaler = -1
            if self.putcall == 'Put':
                self.type = 1
            else:
                self.type = 0

            self.array = np.array(
                [[self.scaler, self.type, self.spot, self.strike, self.exp, self.iv,
                  self.sw, self.ss, self.ts]],
                np.float64
            )
            self.main_array[counter] = self.array
            counter += 1

        self.df = main_array(self.main_array, self.target)
        self.x = self.df.columns.values
        self.y = self.df.index.values
        Z = self.df.values
        
        X,Y=np.meshgrid(self.x,self.y)

        #title = self.target + " for " + str(self.strike) + " " + "Call with " + str(self.iv*100) + "% IV" + " and " + str(self.exp) + " DTE"
        self.ThreeDWin.DrawGraph(X, Y, Z, self.target)     


#### PyQt5 GUI ####
class MainWindow_tri(QWidget):
    def __init__(self, parent = None):

        super(MainWindow_tri,self).__init__()

    ## GRID LAYOUT
        self.layout = QGridLayout()
        self.input_frame = QtWidgets.QFrame()
        self.input_layout = QGridLayout()

        
        self.ThreeDWin = ThreeDSurface_GraphWindow()
        self.layout.addWidget(self.ThreeDWin, 2, 0, 1, 4)

        self.layout_button = QPushButton('Toggle Inputs', self)
        self.layout.addWidget(self.layout_button, 3, 0)
        self.layout_button.clicked.connect(self.toggle_inputs)

        self.export_df_button = QPushButton('Export CSV', self)
        self.layout.addWidget(self.export_df_button, 3, 1)
        self.export_df_button.clicked.connect(self.export_df)

        self.export_df_button = QPushButton('Export PNG', self)
        self.layout.addWidget(self.export_df_button, 3, 2)
        self.export_df_button.clicked.connect(self.export_jpg)

        my_range = [0,2,4]
        counter = 1
        for i in my_range:

            self.contract_label = QLabel(self)
            self.contract_label.setText("Contract {}:".format(counter))
            self.input_layout.addWidget(self.contract_label, i, 0)
            counter += 1
            
            self.strike_input_label = QLabel(self)
            self.strike_input_label.setText("Strike: ")
            self.strike_input_label.setStyleSheet('color: black')
            self.input_layout.addWidget(self.strike_input_label, i, 1)
            self.strike_input = QLineEdit(self)
            objname = "strike_{}".format(str(i))
            self.strike_input.setObjectName(objname)
            self.input_layout.addWidget(self.strike_input, i, 2)

            if i == 0:
                self.spot_input_label = QLabel(self)
                self.spot_input_label.setText("Spot: ")
                self.spot_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.spot_input_label, i, 3)
                self.spot_input = QLineEdit(self)
                objname = "spot_{}".format(str(i))
                self.spot_input.setObjectName(objname)
                self.input_layout.addWidget(self.spot_input, i, 4)
            if i == 0:
                self.exp_input_label = QLabel(self)
                self.exp_input_label.setText("DTE: ")
                self.exp_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.exp_input_label, i, 5)
                self.exp_input = QLineEdit(self)
                objname = "exp_{}".format(str(i))
                self.exp_input.setObjectName(objname)
                self.input_layout.addWidget(self.exp_input, i, 6)

            self.iv_input_label = QLabel(self)
            self.iv_input_label.setText("IV: ")
            self.iv_input_label.setStyleSheet('color: black')
            self.input_layout.addWidget(self.iv_input_label, i, 7)
            self.iv_input = QLineEdit(self)
            objname = "iv_{}".format(str(i))
            self.iv_input.setObjectName(objname)
            self.input_layout.addWidget(self.iv_input, i, 8)

            if i == 0:
                
                self.r_input_label = QLabel(self)
                self.r_input_label.setText("R: ")
                self.r_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.r_input_label, i, 9)
                self.r_input = QLineEdit(self)
                objname = "r_{}".format(str(i))
                self.r_input.setObjectName(objname)
                self.input_layout.addWidget(self.r_input, i, 10)

            self.longshort_comboBox = QComboBox(self)
            self.longshort_comboBox.setObjectName(("comboBox"))
            self.longshort_comboBox.addItem("Long")
            self.longshort_comboBox.addItem("Short")
            objname = "longshort_{}".format(str(i))
            self.longshort_comboBox.setObjectName(objname)
            self.input_layout.addWidget(self.longshort_comboBox, i + 1, 1)

            self.putcall_comboBox = QComboBox(self)
            self.putcall_comboBox.setObjectName(("comboBox"))
            self.putcall_comboBox.addItem("Put")
            self.putcall_comboBox.addItem("Call")
            objname = "putcall_{}".format(str(i))
            self.putcall_comboBox.setObjectName(objname)
            self.input_layout.addWidget(self.putcall_comboBox, i + 1, 2)

        self.contract_label = QLabel(self)
        self.contract_label.setText("Parameters: ")
        self.input_layout.addWidget(self.contract_label, 6, 0)
            
        self.sw_input_label = QLabel(self)
        self.sw_input_label.setText("Spot Width: ")
        self.sw_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.sw_input_label, 6, 1)
        self.sw_input = QLineEdit(self)
        self.input_layout.addWidget(self.sw_input, 6, 2)


        self.ss_input_label = QLabel(self)
        self.ss_input_label.setText("Spot Step: ")
        self.ss_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ss_input_label, 6, 3)
        self.ss_input = QLineEdit(self)
        self.input_layout.addWidget(self.ss_input, 6, 4)

        self.ts_input_label = QLabel(self)
        self.ts_input_label.setText("Time Step: ")
        self.ts_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ts_input_label, 6, 5)
        self.ts_input = QLineEdit(self)
        self.input_layout.addWidget(self.ts_input, 6, 6)

        self.target_label = QLabel(self)
        self.target_label.setText("Target: ")
        self.target_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.target_label, 6, 7)
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("P/L")
        self.comboBox.addItem("Delta")
        self.comboBox.addItem("Gamma")
        self.comboBox.addItem("Theta")
        self.comboBox.addItem("Vega")
        self.input_layout.addWidget(self.comboBox, 6, 8)

        self.button = QPushButton('Submit', self)
        self.input_layout.addWidget(self.button, 6, 10)
        self.button.clicked.connect(self.init_plot)

        self.input_frame.setLayout(self.input_layout)
        self.layout.addWidget(self.input_frame, 0, 0, 1, 4)
        self.setLayout(self.layout)

    def toggle_inputs(self, MainWindow_tri):

        self.input_frame.setHidden(not self.input_frame.isHidden())

    def export_jpg(self, MainWindow_tri):

        
        self.ThreeDWin.fig.savefig('Option3d_fig.png', dpi = self.ThreeDWin.fig.dpi)
      

    def export_df(self, MainWindow_tri):

        try:
            self.df.to_csv("Option3d_data.csv")
        except:
            print("No data to return")

    def init_plot(self, MainWindow_tri):

        my_range = ["0","2", "4"]

        self.ss = float(self.ss_input.text())
        self.sw = float(self.sw_input.text())
        self.ts = float(self.ts_input.text())
        self.exp = float(self.exp_input.text())
        self.r = float(self.r_input.text())
        self.spot = float(self.spot_input.text())
        self.target = str(self.comboBox.currentText())

        self.main_array = np.zeros(shape=(3,9))
        counter = 0
        for i in my_range:
                
            self.strike = float(self.findChild(QtWidgets.QLineEdit, "strike_{}".format(i)).text())
            self.iv = float(self.findChild(QtWidgets.QLineEdit, "iv_{}".format(i)).text())
            self.putcall = str(self.findChild(QtWidgets.QComboBox, "putcall_{}".format(i)).currentText())
            self.longshort = str(self.findChild(QtWidgets.QComboBox, "longshort_{}".format(i)).currentText())

            if self.longshort == 'Long':
                self.scaler = 1
            else:
                self.scaler = -1
            if self.putcall == 'Put':
                self.type = 1
            else:
                self.type = 0

            self.array = np.array(
                [[self.scaler, self.type, self.spot, self.strike, self.exp, self.iv,
                  self.sw, self.ss, self.ts]],
                np.float64
            )
            self.main_array[counter] = self.array
            counter += 1

        self.df = main_array(self.main_array, self.target)
        self.x = self.df.columns.values
        self.y = self.df.index.values
        Z = self.df.values
        
        X,Y=np.meshgrid(self.x,self.y)

        #title = self.target + " for " + str(self.strike) + " " + "Call with " + str(self.iv*100) + "% IV" + " and " + str(self.exp) + " DTE"
        self.ThreeDWin.DrawGraph(X, Y, Z, self.target)

#### PyQt5 GUI ####
class MainWindow_quad(QWidget):
    def __init__(self, parent = None):

        super(MainWindow_quad,self).__init__()

    ## GRID LAYOUT
        self.layout = QGridLayout()
        self.input_frame = QtWidgets.QFrame()
        self.input_layout = QGridLayout()

        
        self.ThreeDWin = ThreeDSurface_GraphWindow()
        self.layout.addWidget(self.ThreeDWin, 2, 0, 1, 4)

        self.layout_button = QPushButton('Toggle Inputs', self)
        self.layout.addWidget(self.layout_button, 3, 0)
        self.layout_button.clicked.connect(self.toggle_inputs)

        self.export_df_button = QPushButton('Export CSV', self)
        self.layout.addWidget(self.export_df_button, 3, 1)
        self.export_df_button.clicked.connect(self.export_df)

        self.export_df_button = QPushButton('Export PNG', self)
        self.layout.addWidget(self.export_df_button, 3, 2)
        self.export_df_button.clicked.connect(self.export_jpg)

        my_range = [0,2,4,6]
        counter = 1
        for i in my_range:

            self.contract_label = QLabel(self)
            self.contract_label.setText("Contract {}:".format(counter))
            self.input_layout.addWidget(self.contract_label, i, 0)
            counter += 1
            
            self.strike_input_label = QLabel(self)
            self.strike_input_label.setText("Strike: ")
            self.strike_input_label.setStyleSheet('color: black')
            self.input_layout.addWidget(self.strike_input_label, i, 1)
            self.strike_input = QLineEdit(self)
            objname = "strike_{}".format(str(i))
            self.strike_input.setObjectName(objname)
            self.input_layout.addWidget(self.strike_input, i, 2)

            if i == 0:
                self.spot_input_label = QLabel(self)
                self.spot_input_label.setText("Spot: ")
                self.spot_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.spot_input_label, i, 3)
                self.spot_input = QLineEdit(self)
                objname = "spot_{}".format(str(i))
                self.spot_input.setObjectName(objname)
                self.input_layout.addWidget(self.spot_input, i, 4)
            if i == 0:
                self.exp_input_label = QLabel(self)
                self.exp_input_label.setText("DTE: ")
                self.exp_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.exp_input_label, i, 5)
                self.exp_input = QLineEdit(self)
                objname = "exp_{}".format(str(i))
                self.exp_input.setObjectName(objname)
                self.input_layout.addWidget(self.exp_input, i, 6)

            self.iv_input_label = QLabel(self)
            self.iv_input_label.setText("IV: ")
            self.iv_input_label.setStyleSheet('color: black')
            self.input_layout.addWidget(self.iv_input_label, i, 7)
            self.iv_input = QLineEdit(self)
            objname = "iv_{}".format(str(i))
            self.iv_input.setObjectName(objname)
            self.input_layout.addWidget(self.iv_input, i, 8)

            if i == 0:
                
                self.r_input_label = QLabel(self)
                self.r_input_label.setText("R: ")
                self.r_input_label.setStyleSheet('color: black')
                self.input_layout.addWidget(self.r_input_label, i, 9)
                self.r_input = QLineEdit(self)
                objname = "r_{}".format(str(i))
                self.r_input.setObjectName(objname)
                self.input_layout.addWidget(self.r_input, i, 10)

            self.longshort_comboBox = QComboBox(self)
            self.longshort_comboBox.setObjectName(("comboBox"))
            self.longshort_comboBox.addItem("Long")
            self.longshort_comboBox.addItem("Short")
            objname = "longshort_{}".format(str(i))
            self.longshort_comboBox.setObjectName(objname)
            self.input_layout.addWidget(self.longshort_comboBox, i + 1, 1)

            self.putcall_comboBox = QComboBox(self)
            self.putcall_comboBox.setObjectName(("comboBox"))
            self.putcall_comboBox.addItem("Put")
            self.putcall_comboBox.addItem("Call")
            objname = "putcall_{}".format(str(i))
            self.putcall_comboBox.setObjectName(objname)
            self.input_layout.addWidget(self.putcall_comboBox, i + 1, 2)

        self.contract_label = QLabel(self)
        self.contract_label.setText("Parameters: ")
        self.input_layout.addWidget(self.contract_label, 8, 0)
            
        self.sw_input_label = QLabel(self)
        self.sw_input_label.setText("Spot Width: ")
        self.sw_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.sw_input_label, 8, 1)
        self.sw_input = QLineEdit(self)
        self.input_layout.addWidget(self.sw_input, 8, 2)


        self.ss_input_label = QLabel(self)
        self.ss_input_label.setText("Spot Step: ")
        self.ss_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ss_input_label, 8, 3)
        self.ss_input = QLineEdit(self)
        self.input_layout.addWidget(self.ss_input, 8, 4)

        self.ts_input_label = QLabel(self)
        self.ts_input_label.setText("Time Step: ")
        self.ts_input_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.ts_input_label, 8, 5)
        self.ts_input = QLineEdit(self)
        self.input_layout.addWidget(self.ts_input, 8, 6)

        self.target_label = QLabel(self)
        self.target_label.setText("Target: ")
        self.target_label.setStyleSheet('color: black')
        self.input_layout.addWidget(self.target_label, 8, 7)
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("P/L")
        self.comboBox.addItem("Delta")
        self.comboBox.addItem("Gamma")
        self.comboBox.addItem("Theta")
        self.comboBox.addItem("Vega")
        self.input_layout.addWidget(self.comboBox, 8, 8)

        self.button = QPushButton('Submit', self)
        self.input_layout.addWidget(self.button, 8, 10)
        self.button.clicked.connect(self.init_plot)

        self.input_frame.setLayout(self.input_layout)
        self.layout.addWidget(self.input_frame, 0, 0, 1, 4)
        self.setLayout(self.layout)

    def toggle_inputs(self, MainWindow_quad):

        self.input_frame.setHidden(not self.input_frame.isHidden())

    def export_jpg(self, MainWindow_quad):

        
        self.ThreeDWin.fig.savefig('Option3d_fig.png', dpi = self.ThreeDWin.fig.dpi)
      

    def export_df(self, MainWindow_quad):

        try:
            self.df.to_csv("Option3d_data.csv")
        except:
            print("No data to return")

    def init_plot(self, MainWindow_quad):

        my_range = ["0","2", "4", "6"]

        self.ss = float(self.ss_input.text())
        self.sw = float(self.sw_input.text())
        self.ts = float(self.ts_input.text())
        self.exp = float(self.exp_input.text())
        self.r = float(self.r_input.text())
        self.spot = float(self.spot_input.text())
        self.target = str(self.comboBox.currentText())

        self.main_array = np.zeros(shape=(4,9))
        counter = 0
        for i in my_range:
                
            self.strike = float(self.findChild(QtWidgets.QLineEdit, "strike_{}".format(i)).text())
            self.iv = float(self.findChild(QtWidgets.QLineEdit, "iv_{}".format(i)).text())
            self.putcall = str(self.findChild(QtWidgets.QComboBox, "putcall_{}".format(i)).currentText())
            self.longshort = str(self.findChild(QtWidgets.QComboBox, "longshort_{}".format(i)).currentText())

            if self.longshort == 'Long':
                self.scaler = 1
            else:
                self.scaler = -1
            if self.putcall == 'Put':
                self.type = 1
            else:
                self.type = 0

            self.array = np.array(
                [[self.scaler, self.type, self.spot, self.strike, self.exp, self.iv,
                  self.sw, self.ss, self.ts]],
                np.float64
            )
            self.main_array[counter] = self.array
            counter += 1

        self.df = main_array(self.main_array, self.target)
        self.x = self.df.columns.values
        self.y = self.df.index.values
        Z = self.df.values
        
        X,Y=np.meshgrid(self.x,self.y)

        #title = self.target + " for " + str(self.strike) + " " + "Call with " + str(self.iv*100) + "% IV" + " and " + str(self.exp) + " DTE"
        self.ThreeDWin.DrawGraph(X, Y, Z, self.target)





class Window(QWidget):

    def __init__(self, parent = None):

        super(Window,self).__init__()

        self.parent_layout = QGridLayout()
        self.setLayout(self.parent_layout)

        self.tabwidget = QtWidgets.QTabWidget()
        self.Tab1 = MainWindow_single()
        self.Tab2 = MainWindow_double()
        self.Tab3 = MainWindow_tri()
        self.Tab4 = MainWindow_quad()
        
        self.tabwidget.addTab(self.Tab1, '1 Leg')
        self.tabwidget.addTab(self.Tab2, '2 Leg')
        self.tabwidget.addTab(self.Tab3, '3 Leg')
        self.tabwidget.addTab(self.Tab4, '4 Leg')
        
        self.parent_layout.addWidget(self.tabwidget, 0,0)
        
        
if __name__ == "__main__":
        App = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(App.exec())
