import os
import sys

import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox

pd.options.display.float_format = '{:.2f}'.format


class Utils:
    def __init__(self):
        pass


def check_path(a):
    if not os.path.exists(a):
        os.makedirs(a)
    else:
        print('Path exists')


def get_dataframe(name):
    return pd.read_csv(name)


def getFileNames(self):
    file_filter = 'All Files (*.*);; Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
    filedialog = QFileDialog()
    response = filedialog.getOpenFileNames(
        parent=self,
        caption='Select a data file',
        directory=os.getcwd(),
        filter=file_filter,
        initialFilter='Excel File (*.xlsx *.xls)'
    )
    print("File Dialog started")
    # filedialog.exec_()
    return response[0]


def getSaveFileName(self):
    file_filter = 'All Files (*.*);; Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
    file_dialog = QFileDialog()
    response = file_dialog.getSaveFileName(
        parent=self,
        caption='Select a data file',
        directory='Data File.dat',
        filter=file_filter,
        initialFilter='Excel File (*.xlsx *.xls)'
    )
    print("Save Dialog started")
    return response[0]


def convert_xls2csv(fileNames):
    print("Converting started")
    processed_files = []
    ll = 0
    names = list(map(lambda x: os.path.basename(x), fileNames))
    for name, path in zip(names, fileNames):
        ll += 1
        if not os.path.exists(f'csv_files/{name[:10]}v{ll}.csv'):
            data_frame = pd.read_excel(f"{path}", index_col=None)
            # data_frame = data_frame[
            #     ['Journal number', 'Date', 'Ledger account', 'Amount', 'Created date and time']]
            data_frame['Ledger account'] = data_frame['Ledger account'].str.slice(0, 6)
            data_frame.to_csv(f'csv_files/' + name[:10] + f'v{ll}.csv', encoding='utf-8',
                              index=False)
            processed_files.append(f'{name[:10]}v{ll}.csv')
            print(name + " processed")
        else:
            processed_files = os.listdir(f'csv_files/')

    if not os.path.exists('converted.csv'):
        # files = [f for f in os.listdir('csv_files') if re.match(r'.*\.cvs', f)]
        # combined_csv = pd.concat([pd.read_csv(f'csv_files/{processed_files}')], join='inner')
        converted = pd.concat([pd.read_csv(f'csv_files/{f}') for f in processed_files])
        converted.sort_values(['Ledger account'], ascending=True, inplace=True)
        converted.to_csv("converted.csv", index=False, encoding='utf-8-sig')
    else:
        print("converted.csv exists")

    return "converted.csv"


def output_result_csv(name, dataframe, column_name):
    check_path('results')
    dataframe_main = pd.read_csv('converted.csv')
    dataframe = pd.DataFrame(dataframe, columns=[column_name])
    # temp = pd.DataFrame({column_name: temp})
    # temp.reset_index(drop=True, inplace=True)
    # dataframe_main.reset_index(drop=True, inplace=True)

    # dataframe = dataframe_main.merge(dataframe, how='inner')
    dataframe = dataframe_main.loc[
        dataframe_main['Journal number'].isin(dataframe['Journal number'].tolist())]
    dataframe.to_csv(f'results/{name}.csv', index=False, encoding='utf-8')


def programExit(self):
    quit_msg = "Are you sure you want to exit the program?"
    reply = QMessageBox.question(self, 'PyQt5 message', quit_msg,
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        QApplication.instance().quit()
    else:
        pass
        # QMessageBox.information(self, '', "Nothing Changed")


def run_on_excel(name):
    os.system(f'start excel.exe {os.path.abspath(name)}')


def info_message(self, text):
    QMessageBox.information(self, '', f'{text}')
