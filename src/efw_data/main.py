import os
import sys

from PyQt5.QtWidgets import QApplication
# from pyproj import _datadir, datadir

from interface import MainWindow

path_FatigueKomplett = os.getcwd() + "/input_data_v1.0.xlsb"
path_FR_STR = os.getcwd() + "/input_data/Frames_and_stringers.csv"
path_PAX_to_GMF = os.getcwd() + "/input_data/frames.csv"
path_Cs = os.getcwd() + "/input_data/Cs_factors.csv"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())