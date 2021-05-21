# from PyQt5 import uic
# from PyQt5.uic.properties import QtGui
import sys

# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, QMessageBox
# from PyQt5.uic.properties import QtGui, QtCore
from functools import cached_property

from PyQt5 import QtWidgets, uic

# back_forward_date_entries = uic.loadUiType("back_forward_date_entries.ui")[0]
# out_of_bound_entries = uic.loadUiType("out_of_bound_entries.ui")[0]
# weekend_entries = uic.loadUiType("weekend_entries.ui")[0]
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget


class BackForwardUI(QDialog):
    def __init__(self):
        super(BackForwardUI, self).__init__()
        uic.loadUi('back_forward_date_entries.ui', self)  # Load the .ui file
        # uic.loadUi('user_input_widgets/back_forward_date_entries.ui', self)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi('out_of_bound_entries.ui', self)


class Controller:
    def __init__(self):
        self.stacked_widget.addWidget(self.welcome)
        self.stacked_widget.addWidget(self.login)

        self.welcome.login.clicked.connect(self.goto_login)

    @cached_property
    def stacked_widget(self):
        return QStackedWidget()

    @cached_property
    def welcome(self):
        return BackForwardUI()

    @cached_property
    def login(self):
        return LoginScreen()

    def goto_login(self):
        self.stacked_widget.setCurrentWidget(self.login)


def main(args):
    app = QApplication(args)

    controller = Controller()
    controller.stacked_widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)

# class OutofBoundUI(QtGui.QDialog):
#     def __init__(self, parent=None):
#         QtGui.QDialog.__init__(self, parent)
#         uic.loadUi('user_input_widgets/out_of_bound_entries.ui', self)
#         self.setupUi(self)
#
#
# class WeekendUI(QtGui.QDialog):
#     def __init__(self, parent=None):
#         QtGui.QDialog.__init__(self, parent)
#         uic.loadUi('user_input_widgets/weekend_entries.ui', self)
#         self.setupUi(self)
