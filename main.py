# This is a sample Python script.
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic.properties import QtGui, QtCore

import utils
from show_csv import MainWindow
# from user_input_widgets.user_input_dialogs import BackForwardUI, OutofBoundUI, WeekendUI
from utils import *
from checking_data import *
from PyQt5 import QtWidgets, uic
import sys
import os


class Ui(QtWidgets.QMainWindow):
    fileNames = ""
    all_data_csv = ""
    response = ""
    dataframe = ""

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.pb_test.setEnabled(False)
        self.w = None  # No external window yet.
        self.UiComponents()

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        # self.actionSave_as.triggered.connect(self.quitApp)
        self.actionClose.triggered.connect(self.clearNames)
        self.actionExit.triggered.connect(self.quitApp)
        # self.actionFAQ.triggered.connect(self.quitApp)
        # self.actionAbout_App.triggered

        self.pb_open.clicked.connect(self.openFile)
        self.pb_clear.clicked.connect(self.clearNames)
        # self.pb_preprocess.clicked.connect(self.preProcessing)
        self.pb_viewdata.clicked.connect(self.viewData)
        self.pb_initial_test.clicked.connect(self.initial_testing)
        self.pb_test.clicked.connect(self.test_selected_item)

    def openFile(self):
        self.fileNames = getFileNames(self)
        # self.fileNames = list(map(lambda x: os.path.basename(x), self.fileNames))
        # print(self.fileNames)
        self.all_data_csv = convert_xls2csv(self.fileNames)
        QMessageBox.information(self, '', "All files processed")
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
        for f in os.listdir('csv_files'):
            os.remove(os.path.join('csv_files', f))
            print(f'all files in folder csv_files are deleted successfully')
            # os.remove(os.path.join(root, file))
        if os.path.exists('converted.csv'):
            os.remove('converted.csv')
        else:
            print("The file does not exist")
        print("All Files removed")
        info_message(self, "Opened Files dropped")

    def preProcessing(self):
        pass

    def viewData(self):
        path = 'results'
        # open("results/")
        # run_on_excel('converted.csv')
        webbrowser.open(os.path.realpath('results'))
        # os.system(f'start {os.path.realpath(path)}')
        # subprocess.Popen(f'explorer {os.path.realpath(path)}')
        # subprocess.run(['explorer', os.path.realpath(path)])

    def quitApp(self):
        programExit(self)

    def initial_testing(self):
        self.dataframe = get_dataframe(name='converted.csv')
        self.dataframe = init_date(self.dataframe)
        # math_accuracy(self.dataframe)
        # data_integrity_check(self.dataframe)
        info_message(self, "Initial testing done, additional testing is available!")
        self.pb_test.setEnabled(True)

    def UiComponents(self):
        cmb_list_items = ["Finding wrong entries", "Out of bound entries", "Weekend entries",
                          "Holiday entries", "Unusual times", "Back and forward dates entries",
                          "Dismissed employee analysis", "Suspicious description",
                          "Over scope entries", "User analysis", "Treshold analysis"]

        # adding list of items to combo box
        self.cmb_tests.addItems(cmb_list_items)

    def test_selected_item(self):
        item = self.cmb_tests.currentText()
        index = self.cmb_tests.currentIndex()
        if index == 0:
            finding_wrong_entries(self.dataframe)
        if index == 1:
            out_of_bound_entries(self.dataframe)
        if index == 2:
            weekend_entries(self.dataframe)
        if index == 3:
            holiday_entries(self.dataframe)
        if index == 4:
            unusual_times(self.dataframe)
        if index == 5:
            back_forward_date_entries(self.dataframe)
        if index == 6:
            dismissed_employee(self.dataframe)
        if index == 7:
            suspicious_desc(self.dataframe)
        if index == 8:
            over_scope_entries(self.dataframe)
        if index == 9:
            user_analysis(self.dataframe)
        if index == 10:
            treshold_analysis(self.dataframe)
        print(item)
        # print(index)

    def run_dialog(self):
        pass
        # print('run dialog hit')
        # a = BackForwardUI()
        # a.exec()


def main(strings):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{strings}')  # Press Ctrl+F8 to toggle the breakpoint.
    check_path('csv_files')
    check_path('results')


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
