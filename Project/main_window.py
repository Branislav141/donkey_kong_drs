from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget, QComboBox
from PyQt5.QtGui import QPixmap
import sys

from sim_move_demo import SimMoveDemo



class MainWindow(QWidget):
    MainWindowHeight = 1080
    MainWindowWidth = 1920

    def __init__(self):
        super().__init__()
        self.initUI()

    def run(self):
        self.smd = SimMoveDemo()

    def quit(self):
        self.close();

    def initUI(self):
        self.resize(self.MainWindowHeight, self.MainWindowWidth)
        self.center()

        self.setWindowTitle('Donkey Kong')

        self.setMinimumHeight(self.MainWindowHeight)
        self.setMinimumWidth(self.MainWindowWidth)
        self.setMaximumHeight(self.MainWindowHeight)
        self.setMaximumWidth(self.MainWindowWidth)
        self.setStyleSheet("background-color: black;")

        player1Lb = QtWidgets.QLabel(self)
        player1Lb.setText("Select player 1: ")
        player1Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        player1Lb.move(200, 300)

        player1Cb = QComboBox(self)
        player1Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        player1Cb.addItem("")
        player1Cb.addItem("Naruto")
        player1Cb.addItem("Sasuke")
        player1Cb.addItem("Itachi")
        player1Cb.model().item(0).setEnabled(False)
        player1Cb.setGeometry(380, 305, 70, 20)

        player2Lb = QtWidgets.QLabel(self)
        player2Lb.setText("Select player 2: ")
        player2Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        player2Lb.move(200, 350)

        player2Cb = QComboBox(self)
        player2Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        player2Cb.addItem("")
        player2Cb.addItem("Naruto")
        player2Cb.addItem("Sasuke")
        player2Cb.addItem("Itachi")
        player2Cb.model().item(0).setEnabled(False)
        player2Cb.setGeometry(380, 355, 70, 20)

        player3Lb = QtWidgets.QLabel(self)
        player3Lb.setText("Select player 3: ")
        player3Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        player3Lb.move(200, 400)

        player3InfoLb = QtWidgets.QLabel(self)
        player3InfoLb.setText("(Only in tournament!)")
        player3InfoLb.setStyleSheet("color: red;font-size: 14px; font-family: Helvetica;");
        player3InfoLb.move(460, 405)

        player3Cb = QComboBox(self)
        player3Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        player3Cb.addItem("")
        player3Cb.addItem("Naruto")
        player3Cb.addItem("Sasuke")
        player3Cb.addItem("Itachi")
        player3Cb.model().item(0).setEnabled(False)
        player3Cb.setGeometry(380, 405, 70, 20)

        player4Lb = QtWidgets.QLabel(self)
        player4Lb.setText("Select player 3: ")
        player4Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        player4Lb.move(200, 450)

        player4InfoLb = QtWidgets.QLabel(self)
        player4InfoLb.setText("(Only in tournament!)")
        player4InfoLb.setStyleSheet("color: red;font-size: 14px; font-family: Helvetica;");
        player4InfoLb.move(460, 455)

        player4Cb = QComboBox(self)
        player4Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        player4Cb.addItem("")
        player4Cb.addItem("Naruto")
        player4Cb.addItem("Sasuke")
        player4Cb.addItem("Itachi")
        player4Cb.model().item(0).setEnabled(False)
        player4Cb.setGeometry(380, 455, 70, 20)

        gameModeLb = QtWidgets.QLabel(self)
        gameModeLb.setText("Select game mode: ")
        gameModeLb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        gameModeLb.move(200, 525)

        versusRb = QtWidgets.QRadioButton(self)
        versusRb.setText("Versus")
        versusRb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        versusRb.move(390, 522)
        versusRb.setChecked(True)

        tournamentRb = QtWidgets.QRadioButton(self)
        tournamentRb.setText("Tournament")
        tournamentRb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        tournamentRb.move(490, 522)
        tournamentRb.setChecked(False)


        b1 = QtWidgets.QPushButton(self)
        b1.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        b1.setText("START GAME")
        b1.setGeometry(200, 600, 350, 50)
        b1.clicked.connect(self.run)

        b2 = QtWidgets.QPushButton(self)
        b2.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        b2.setText("QUIT")
        b2.setGeometry(200, 700, 350, 50)
        b2.clicked.connect(self.quit)

        self.logoPic = QPixmap('images\menu\donkey_logo.png')
        self.logoLabel = QtWidgets.QLabel(self)
        self.logoLabel.setPixmap(self.logoPic)
        self.logoLabel.move(880, 120)

        self.monkeyPic = QPixmap('images\menu\donkey_monkey.png')
        self.monkeyLabel = QtWidgets.QLabel(self)
        self.monkeyLabel.setPixmap(self.monkeyPic)
        self.monkeyLabel.move(970, 300)

        self.showMaximized()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
