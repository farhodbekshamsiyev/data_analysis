# This is a sample Python script.
import os
import shutil
import subprocess
import sys
import webbrowser
import platform

from PyQt5 import QtWidgets, uic

from checking_data import *
from TabWidget import TabWidget


class Ui(QtWidgets.QMainWindow):
    fileNames = ""
    fileNames_gl = []
    fileNames_tb = []
    all_data_csv = ""
    response = ""
    dataframe = ""
    dir_name = ""

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('user_interface/main.ui', self)
        # self.setWindowIcon(QIcon('images/pkf.png'))

        self.pb_additional_test.setEnabled(False)

        self.actionOpen.triggered.connect(self.loadGl)
        self.actionDrop.triggered.connect(self.clearNames)
        self.actionQuit.triggered.connect(self.quitApp)
        self.actionResults.triggered.connect(self.viewData)
        self.listWidget.currentItemChanged.connect(self.initial_testing)
        # self.actionFAQ.triggered.connect(self.quitApp)
        # self.actionAbout.triggered.connect(self.quitApp)

        # self.pb_loadgl.clicked.connect(self.loadGl)
        # self.pb_loadtb.clicked.connect(self.loadTb)
        # self.pb_clear.clicked.connect(self.clearNames)
        # self.pb_preprocess.clicked.connect(self.preProcessing)
        # self.pb_viewdata.clicked.connect(self.viewData)
        # self.pb_initial_test.clicked.connect(self.initial_testing)
        self.pb_additional_test.clicked.connect(self.additional_tests)

        # info_message(self, "Starting")

    def loadGl(self):
        self.listWidget.clear()
        self.fileNames_gl = getFileNames(self)
        if not self.fileNames_gl:
            info_message(self, '0 files are selected')
            return
        # self.fileNames_gl.extend(files)
        # self.listWidget.clear()
        if self.fileNames_gl:
            self.dir_name = self.fileNames_gl[0].split('/')[-2]
            print(self.dir_name)
            print(self.fileNames_gl)
            # self.all_data_csv = convert_xls2csv(self.fileNames, "gl_files", "conv_GL")
            self.listWidget.addItems(map(lambda x: os.path.basename(x), self.fileNames_gl))
        # self.fileNames = list(map(lambda x: os.path.basename(x), self.fileNames))
        # print(self.fileNames)
        # QMessageBox.information(self, '', "All files processed")
        # print(self.response)

    def loadTb(self):
        self.fileNames_tb = getFileNames(self)
        self.dir_name = self.fileNames_tb[0].split('/')[-2]
        if self.fileNames_tb:
            # self.all_data_csv = convert_xls2csv(self.fileNames, "tb_files", "conv_TB", True)
            self.listWidget.addItems(map(lambda x: os.path.basename(x), self.fileNames_tb))
        # self.fileNames = list(map(lambda x: os.path.basename(x), self.fileNames))
        # print(self.fileNames)
        # QMessageBox.information(self, '', "All files processed")
        # print(self.response)

    def process_gl(self):
        if self.fileNames_gl:
            # Preprocessor.delete_rows_and_spaces(self.fileNames_gl, 3, 1)
            # Preprocessor.clear_formats(self.fileNames_gl)
            # Preprocessor.xls_to_csv(self.fileNames_gl)
            self.run_test(self.fileNames_gl)
        else:
            info_message(self, "Choose General ledger files first!")

    def concatenate_excels(self, files):
        name = files[0].split('/')[-1]
        print(name)
        check_path('merged')
        folder = files[0].split('/')[-2]
        print(folder)
        df = pd.concat([pd.read_excel(file) for file in files])
        df.to_excel(f'merged/{name[:7]}.xlsx', index=False, encoding='utf-8-sig')
        info_message(self, "Concatenation finished successfully!")
        print('Concatenation finished successfully')

    def saveFile(self):
        self.fileNames = getSaveFileName(self)
        response = list(map(lambda x: os.path.basename(x), self.fileNames))
        # print(self.fileNames)
        print(response)

    def clearNames(self):
        self.fileNames_gl = ""
        self.fileNames_tb = ""
        info_message(self, "Opened Files dropped")
        self.listWidget.clear()
        self.pb_additional_test.setEnabled(False)
        # for f in os.listdir('gl_files'):
        #     os.remove(os.path.join('gl_files', f))
        #     print(f'all files in folder gl_files are deleted successfully')
        #     # os.remove(os.path.join(root, file))
        #
        # for f in os.listdir('tb_files'):
        #     os.remove(os.path.join('tb_files', f))
        #     print(f'all files in folder tb_files are deleted successfully')
        #     # os.remove(os.path.join(root, file))

        # if os.path.exists('conv_GL.csv'):
        #     os.remove('conv_GL.csv')
        # elif os.path.exists('conv_TB.csv'):
        #     os.remove('conv_TB.csv')
        # else:
        #     print("The file does not exist")
        # print("All Files removed")

    def preProcessing(self):
        pass

    def viewData(self):
        path = 'results'
        print(platform.system())
        if platform.system().lower()[:3] == 'win':
            subprocess.Popen(f'explorer {os.path.realpath(path)}')
            subprocess.run(['explorer', os.path.realpath(path)])
        else:
            webbrowser.open(os.path.realpath('results'))

    def quitApp(self):
        app_quit(self)

    def initial_testing(self):
        # self.dataframe = get_dataframe(name='conv_GL.csv')
        # self.dataframe = init_date(self.dataframe)
        # data_integrity_check(self.dataframe)
        # math_accuracy(self.dataframe)
        # finding_wrong_entries(self.dataframe)
        if self.fileNames_gl:
            info_message(self, 'Files are loaded!')
            self.pb_additional_test.setEnabled(True)
            for f in os.listdir('results'):
                if os.path.isfile(f):
                    os.remove(os.path.join('results', f))
                else:
                    shutil.rmtree(os.path.join('results', f))
            print(f'all files in folder results are deleted successfully')
        else:
            info_message(self, 'Please load general ledger files!')

    def additional_tests(self):
        TabWidget(self.fileNames_gl).show()


def main(strings):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{strings}')  # Press Ctrl+F8 to toggle the breakpoint.
    # check_path('gl_files')
    # check_path('tb_files')
    check_path('results')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pd.set_option('display.max_rows', None)
    main('Program starts')

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
