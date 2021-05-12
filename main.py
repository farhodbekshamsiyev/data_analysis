# This is a sample Python script.
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic.properties import QtGui, QtCore

import utils
from show_csv import MainWindow
from utils import *
from checking_data import *
from PyQt5 import QtWidgets, uic
import sys


class Ui(QtWidgets.QMainWindow):
    fileNames = ""
    all_data_csv = ""
    response = ""

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        self.w = None  # No external window yet.

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        # self.actionSave_as.triggered.connect(self.quitApp)
        self.actionClose.triggered.connect(self.clearNames)
        self.actionExit.triggered.connect(self.quitApp)
        # self.actionFAQ.triggered.connect(self.quitApp)
        # self.actionAbout_App.triggered

        self.pb_open.clicked.connect(self.openFile)
        self.pb_clear.clicked.connect(self.clearNames)
        self.pb_preprocess.clicked.connect(self.preProcessing)
        self.pb_viewdata.clicked.connect(self.viewData)

    def openFile(self):
        self.fileNames = getFileNames(self)
        # self.fileNames = list(map(lambda x: os.path.basename(x), self.fileNames))
        # print(self.fileNames)
        self.listWidget.addItems(map(lambda x: os.path.basename(x), self.fileNames))
        # print(self.response)

    def saveFile(self):
        self.fileNames = getSaveFileName(self)
        response = list(map(lambda x: os.path.basename(x), self.fileNames))
        # print(self.fileNames)
        print(response)

    def clearNames(self):
        self.listWidget.clear()
        self.fileNames = ""
        print("Opened Files dropped")
        QMessageBox.information(self, '', "Opened Files dropped")

    def preProcessing(self):
        self.all_data_csv = convert_xls2csv(self.fileNames)
        QMessageBox.information(self, '', "All files processed Changed")

    def viewData(self):
        self.w = MainWindow()
        self.w.show()
        if self.w is None:
            pass
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def quitApp(self):
        programExit(self)


def main(strings):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{strings}')  # Press Ctrl+F8 to toggle the breakpoint.
    check_path('csv_files')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pd.set_option('display.max_rows', None)
    main('Program starts')

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())

    # csv_name = convert_xls2csv('csv_files')
    # dataframe = pd.read_csv(csv_name)
    # dataframe = init_date(dataframe=dataframe)
    # print(dataframe)
    # completness_check('combined.csv')
    # math_accuracy(dataframe)
    # data_integrity_check(dataframe)
    # finding_wrong_entries(dataframe)
    # out_of_bound_entries(dataframe)
    # weekend_entries(dataframe)
    # holiday_entries(dataframe)
    # unusual_times(dataframe)
    # back_forward_date_entries(dataframe)
    # dismissed_employee(dataframe)
    # suspicious_desc(dataframe)
    # over_scope_entries(dataframe)
    # user_analysis(dataframe)
    # treshold_analysis(dataframe)

    # whole_amounts(dataframe)
    # reversal_entries(dataframe)
