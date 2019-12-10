import sys

from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

from key_notifier import KeyNotifier
import datetime

class SimMoveDemo(QWidget):

    def __init__(self):
        super().__init__()

        #background image
        self.backgroundPicture = QPixmap('images\level\\background.png')
        self.backgroundLabel = QLabel(self)




        self.pix1 = QPixmap('mario1.png')
        self.pix2 = QPixmap('skull_green.png')
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        self.movie1 = QMovie("right.gif");
        self.movie2 = QMovie("left.gif");
        self.pix3 = QPixmap('penjanje.png')



        self.setWindowState(Qt.WindowMaximized)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def __init_ui__(self):

        self.backgroundLabel.setPixmap(self.backgroundPicture)
        self.backgroundLabel.move(0, 0)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(100, 997, 100, 100)


        self.label2.setPixmap(self.pix2)
        self.label2.setGeometry(50, 40, 50, 50)





        self.setWindowTitle('Sim Slide')
        self.showFullScreen()

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        self.key_notifier.rem_key(event.key())
        self.label1.setPixmap(self.pix1)

    def __update_position__(self, key):
        rec1 = self.label1.geometry()
        rec2 = self.label2.geometry()

        if key == Qt.Key_Right:
            self.label1.setMovie(self.movie1);
            self.movie1.start();
            self.label1.setGeometry(rec1.x() + 5, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Down:
            self.label1.setPixmap(self.pix3)
            self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            self.label1.setPixmap(self.pix3)
            self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Left:
            self.label1.setMovie(self.movie2);
            self.movie2.start();
            self.label1.setGeometry(rec1.x() - 5, rec1.y(), rec1.width(), rec1.height())

        if key == Qt.Key_D:
            self.label2.setGeometry(rec2.x() + 5, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_S:
            self.label2.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
        elif key == Qt.Key_W:
            self.label2.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
        elif key == Qt.Key_A:
            self.label2.setGeometry(rec2.x() - 5, rec2.y(), rec2.width(), rec2.height())

    def closeEvent(self, event):
        self.key_notifier.die()


