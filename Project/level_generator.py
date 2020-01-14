import sys
import time
from threading import Thread


from PyQt5.QtCore import Qt, QTime, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton


from key_notifier import KeyNotifier
from Character import Character
from Gorilla import Gorilla


import datetime
import random


# list of values of Y axis where characters can move
listOfValidYAxisValues = [950, 951, 952, 750, 751, 752, 550, 551, 552, 350, 351, 352, 150, 151, 152, 0, 1, 2]
listOfSoundtracks = ["song_hyouhaku", "song_kokuten", "song_raising_fighting_spirit", "song_saika", "song_senya", "song_madara_theme"]

class LevelGenerator(QWidget):

    player1Points = 0
    player2Points = 0
    currentLevel = 0

    gameIsOver = False
    checkCollisionSignal = pyqtSignal()
    callEndLevel = pyqtSignal()

    def __init__(self, gameMode, player1, player2, player3, player4):
        super().__init__()
        self.forceThreadRun()
        self.newLevel(gameMode, player1, player2, player3, player4)




    def forceThreadRun(self):
        forceThread = Thread(target=self.initForce__)
        forceThread.setDaemon(True)
        if not(forceThread.isAlive()):
            forceThread.start()


    def initForce__(self):
        arrayOfValidYAxisValues = [760, 560, 360, 160]
        while True:
            time.sleep(10)
            self.forceLabel.show()
            y = random.sample(arrayOfValidYAxisValues, 1)  # dobijamo jednu vrednost iz niza
            y = y[0]
            x = random.randint(100, 1720)  # X MOZE BITI OD 100 DO 1720 BILO KOJI BROj
            self.forceLabel.setFixedSize(60,60)
            self.forceLabel.move(x,y)
            for j in range(0,70):
                self.catchUpForce()
                time.sleep(0.1)
            self.forceLabel.hide()

    def catchUpForce(self):
        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()
        recForce = self.forceLabel.geometry()
        x1 = rec1.x()
        y1 = rec1.y()
        x2 = rec2.x()
        y2 = rec2.y()
        x = recForce.x()
        y = recForce.y()
        if (x1 - 40) <= (x) <= (x1 + 40):
            if (y1 - 15) <= (y) <= (y1 + 15):
                self.player1.korak=20
                self.forceLabel.move(100, 0)
                self.forceLabel.hide()
                time.sleep(6) #vreme trajanja sile
                self.player1.korak = 10
        elif (x2 - 40) <= (x) <= (x2 + 40): #elif da ne bi i ovaj karakter pokupio istu silu posle prvog
            if (y2 - 15) <= (y) <= (y2 + 15):
                self.player2.korak=20
                self.forceLabel.move(100, 0)
                self.forceLabel.hide()
                time.sleep(6) #vreme trajanja sile
                self.player2.korak = 10

    def pointCounterHandle(self):
        # args[750] - prve merdevine
        player1PointCounterThread = Thread(target=self.player1PointCounter__, args=[750])
        player1PointCounterThread.setDaemon(True)
        player1PointCounterThread.start()

        player2PointCounterThread = Thread(target=self.player2PointCounter__, args=[750])
        player2PointCounterThread.setDaemon(True)
        player2PointCounterThread.start()


    def player1PointCounter__(self, y):
        while True:
            time.sleep(0.5)
            rec1 = self.player1.playerLabel.geometry()
            if rec1.y() <= y:
                break
        self.player1.playerPoints += 1
        self.player1.pointsLabel.setText(str(self.player1.playerPoints))
        callbackThread = Thread(target=self.player1PointCounter__, args=[y - 200])
        callbackThread.setDaemon(True)
        callbackThread.start()

    def player2PointCounter__(self, y):
        while True:
            time.sleep(0.5)
            rec2 = self.player2.playerLabel.geometry()
            if rec2.y() <= y:
                break
        self.player2.playerPoints += 1
        self.player2.pointsLabel.setText(str(self.player2.playerPoints))
        callbackThread = Thread(target=self.player2PointCounter__, args=[y - 200])
        callbackThread.setDaemon(True)
        callbackThread.start()


    def levelIntroHandle(self):
        countdownThread = Thread(target=self.countdown__)
        countdownThread.setDaemon(True)
        countdownThread.start()
        self.player1.playerIntroRight.finished.connect(self.char1Intro)
        self.player2.playerIntroLeft.finished.connect(self.char2Intro)

    def winner1Trigger__(self):
        self.gameIsOver = True
        self.player1.winnerLabel.show()
        self.player1.playerPoints += 2
        self.player1.pointsLabel.setText(str(self.player1.playerPoints))
        self.key_notifier.die()
        self.player1.playerLabel.setMovie(self.player1.playerWin)
        self.player1.playerWin.start()
        self.player1.playerWinQuote.play()

        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()

        if not self.checkLeftRight(rec2.y()):
            self.player2.playerLabel.setPixmap(self.player2.playerClimbPicture)
        else:
            if rec1.x() >= rec2.x():
                self.player2.playerLabel.setMovie(self.player2.playerIdleRight)
                self.player2.playerIdleRight.start()
            else:
                self.player2.playerLabel.setMovie(self.player2.playerIdleLeft)
                self.player2.playerIdleLeft.start()



        self.player1Points = self.player1.playerPoints
        self.player2Points = self.player2.playerPoints
        self.forceLabel.hide()

        waitForEndThread = Thread(target=self.waitForEnd__)
        waitForEndThread.setDaemon(True)
        waitForEndThread.start()



    def waitForEnd__(self):
        time.sleep(5)
        self.callEndLevel.emit()

    def goToNextLevel(self):
        self.exitLevel()
        self.newLevel(self.gameMode, self.player1Chr1, self.player2Chr2, self.player3Chr3, self.player4Chr4)

    def winner2Trigger__(self):
        self.gameIsOver = True
        self.player2.winnerLabel.show()
        self.player2.playerPoints += 2
        self.player2.pointsLabel.setText(str(self.player2.playerPoints))
        self.key_notifier.die()
        self.player2.playerLabel.setMovie(self.player2.playerWin)
        self.player2.playerWin.start()
        self.player2.playerWinQuote.play()

        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()

        if not self.checkLeftRight(rec1.y()):
            self.player1.playerLabel.setPixmap(self.player1.playerClimbPicture)
        else:
            if rec1.x() >= rec2.x():
                self.player1.playerLabel.setMovie(self.player1.playerIdleLeft)
                self.player1.playerIdleLeft.start()
            else:
                self.player1.playerLabel.setMovie(self.player1.playerIdleRight)
                self.player1.playerIdleRight.start()


        self.player1Points = self.player1.playerPoints
        self.player2Points = self.player2.playerPoints
        self.forceLabel.hide()
        
        waitForEndThread = Thread(target=self.waitForEnd__)
        waitForEndThread.setDaemon(True)
        waitForEndThread.start()

    def char1Intro(self):
        self.player1.playerLabel.setMovie(self.player1.playerIdleRight)
        self.player1.playerIdleRight.start()

    def char2Intro(self):
        self.player2.playerLabel.setMovie(self.player2.playerIdleLeft)
        self.player2.playerIdleLeft.start()


    def countdown__(self):
        time.sleep(2)
        self.countdownLabel.show()
        time.sleep(1)
        self.countdownLabel.setPixmap(self.cdnTwo)
        time.sleep(1)
        self.countdownLabel.setPixmap(self.cdnOne)
        time.sleep(1)
        self.countdownLabel.hide()
        self.startLabel.show()
        time.sleep(2)
        self.startLabel.hide()



    def newLevel(self, mode, character1, character2, character3, character4):
        self.callEndLevel.connect(self.goToNextLevel)
        if mode=="versus":

            self.gameIsOver = False
            self.gameMode=mode
            self.player1Chr1=character1
            self.player2Chr2 = character2
            self.player3Chr3 = character3
            self.player4Chr4 = character4

            self.setLevelDesign()
            self.setLevelSoundtrack()
            #self.initForce()
            self.initPlayers(character1, character2)
            self.initGorilla()
            self.initCheckCollisions()
            #self.forceThreadRun()
            self.showFullScreen()
            self.levelIntroHandle()

            self.key_notifier = KeyNotifier()
            self.key_notifier.key_signal.connect(self.__update_position__)
            self.key_notifier.start()

            self.player1.winnerSignal.connect(self.winner1Trigger__)
            self.player2.winnerSignal.connect(self.winner2Trigger__)

            self.pointCounterHandle()
        else: #ako je turnir

            self.currentLevel += 1

            self.gameIsOver = False
            self.gameMode = mode
            self.player1Chr1 = character1
            self.player2Chr2 = character2
            self.player3Chr3 = character3
            self.player4Chr4 = character4

            if self.currentLevel == 1: #u prvom nivou prva dva igraca

                self.setLevelDesign()
                self.setLevelSoundtrack()
                # self.initForce()
                self.initPlayers(character1, character2)
                self.initGorilla()
                self.initCheckCollisions()
                # self.forceThreadRun()
                self.showFullScreen()
                self.levelIntroHandle()

                self.key_notifier = KeyNotifier()
                self.key_notifier.key_signal.connect(self.__update_position__)
                self.key_notifier.start()

                self.player1.winnerSignal.connect(self.winner1Trigger__)
                self.player2.winnerSignal.connect(self.winner2Trigger__)

                self.pointCounterHandle()

            elif self.currentLevel == 2: #u drugom nivou druga dva igraca
                if self.player1Points > self.player2Points:
                    self.winner1Chr = self.player1Chr1
                else:
                    self.winner1Chr = self.player2Chr2

                self.player1Points = 0
                self.player2Points = 0

                self.setLevelDesign()
                self.setLevelSoundtrack()
                # self.initForce()
                self.initPlayers(character3, character4)
                self.initGorilla()
                self.initCheckCollisions()
                # self.forceThreadRun()
                self.showFullScreen()
                self.levelIntroHandle()

                self.key_notifier = KeyNotifier()
                self.key_notifier.key_signal.connect(self.__update_position__)
                self.key_notifier.start()

                self.player1.winnerSignal.connect(self.winner1Trigger__)
                self.player2.winnerSignal.connect(self.winner2Trigger__)

                self.pointCounterHandle()

            elif self.currentLevel == 3:  #u trecem nivou dprethodni pobednici
                if self.player1Points > self.player2Points:
                    self.winner2Chr = self.player3Chr3
                else:
                    self.winner2Chr = self.player4Chr4

                self.player1Points = 0
                self.player2Points = 0


                self.setLevelDesign()
                self.setLevelSoundtrack()
                # self.initForce()
                self.initPlayers( self.winner1Chr,  self.winner2Chr)
                self.initGorilla()
                self.initCheckCollisions()
                # self.forceThreadRun()
                self.showFullScreen()
                self.levelIntroHandle()

                self.key_notifier = KeyNotifier()
                self.key_notifier.key_signal.connect(self.__update_position__)
                self.key_notifier.start()

                self.player1.winnerSignal.connect(self.winner1Trigger__)
                self.player2.winnerSignal.connect(self.winner2Trigger__)

                self.pointCounterHandle()







    def setLevelDesign(self):

        self.reset = QPixmap('images\characters\\reset.png')

        # background image
        self.backgroundPicture = QPixmap('images\level\\background.png')
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setPixmap(self.backgroundPicture)
        self.backgroundLabel.move(0, 0)

        # countdown
        self.cdnOne = QPixmap('images\level\one.png')
        self.cdnTwo = QPixmap('images\level\\two.png')
        self.cdnThree = QPixmap('images\level\\three.png')
        self.countdownLabel = QLabel(self)
        self.countdownLabel.hide()
        self.countdownLabel.setPixmap(self.cdnThree)
        self.countdownLabel.move(755, 300)

        # begin
        self.startPicture = QPixmap('images\level\\begin.png')
        self.startLabel = QLabel(self)
        self.startLabel.hide()
        self.startLabel.setPixmap(self.startPicture)
        self.startLabel.move(585, 300)

        #  princess
        self.princessIdle = QMovie('images\\npc\\npc_flame_princess\\npc_flame_princess_idle.gif')
        self.princessLabel = QLabel(self)
        #self.princessLabel.setStyleSheet("background-color: lime;")
        self.princessLabel.setMovie(self.princessIdle)
        self.princessIdle.start()
        self.princessLabel.move(1150, 0)

        #force
        self.forceIdle = QMovie('images\\forces\\force.gif')
        self.forceLabel = QLabel(self)
        self.forceLabel.setMovie(self.forceIdle)
        self.forceIdle.start()


        self.setWindowState(Qt.WindowMaximized)

    def setLevelSoundtrack(self):
        self.song = random.choice(listOfSoundtracks)
        self.levelMusic = QSound("sounds\level\\" + self.song + ".wav")
        self.levelMusic.setLoops(-1)
        self.levelMusic.play()


    def initPlayers(self, chr1, chr2):
        self.player1 = Character(self, 100, 150, chr1, self.player1Points)
        self.player2 = Character(self, 1720, 150, chr2, self.player2Points)

    def initGorilla(self):
        self.gorilla = Gorilla(self)
        self.gorilla.gorillaMoveSpeed += 2 * self.currentLevel
        self.gorilla.barrelMoveSpeed += 2 * self.currentLevel
        self.gorilla.leftDirectionSignal.connect(self.gorilla.leftDirectionGifSetup)
        self.gorilla.rightDirectionSignal.connect(self.gorilla.rightDirectionGifSetup)
        self.gorilla.updatePositionSignal.connect(self.gorilla.updatePosition)
        self.gorilla.createBarrelSignal.connect(self.gorilla.createBarrel)
        self.gorilla.moveBarrelsSignal.connect(self.gorilla.moveBarrels)
        self.gorillaThread = Thread(target=self.gorilla.startRunning)
        self.gorillaThread.setDaemon(True)
        self.gorillaThread.start()


    def keyPressEvent(self, event):
        if event.isAutoRepeat() or self.gameIsOver == True:
            return

        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat() or self.gameIsOver == True:
            return
        self.key_notifier.rem_key(event.key())

        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()

        if not self.checkLeftRight(rec1.y()):
            self.player1.playerLabel.setPixmap(self.player1.playerClimbPicture)
        else:
            if rec1.x() >= rec2.x():
                self.player1.playerLabel.setMovie(self.player1.playerIdleLeft)
                self.player1.playerIdleLeft.start()
            else:
                self.player1.playerLabel.setMovie(self.player1.playerIdleRight)
                self.player1.playerIdleRight.start()

        if not self.checkLeftRight(rec2.y()):
            self.player2.playerLabel.setPixmap(self.player2.playerClimbPicture)
        else:
            if rec1.x() >= rec2.x():
                self.player2.playerLabel.setMovie(self.player2.playerIdleRight)
                self.player2.playerIdleRight.start()
            else:
                self.player2.playerLabel.setMovie(self.player2.playerIdleLeft)
                self.player2.playerIdleLeft.start()

    # check if character can move up
    def checkLadderUp(self, x, y):
        if 900 <= x <= (900 + 20) and y >= 751:
            return True
        elif 115 <= x <= (115 + 20) and 551 <= y <= 751:
            return True
        elif 1732 <= x <= (1732 + 20) and 351 <= y <= 551:
            return True
        elif 323 <= x <= (323 + 20) and 151 <= y <= 351:
            return True
        elif 900 <= x <= (900 + 20) and 10 <= y <= 151:
            return True
        else:
            return False

    # check if character can move down
    def checkLadderDown(self, x, y):
        if 900 <= x <= (900 + 20) and y >= 749:
            return True
        elif 115 <= x <= (115 + 20) and 549 <= y <= 749:
            return True
        elif 1732 <= x <= (1732 + 20) and 349 <= y <= 549:
            return True
        elif 323 <= x <= (323 + 20) and 149 <= y <= 349:
            return True
        elif 900 <= x <= (900 + 20) and -1 <= y <= 149:
            return True
        else:
            return False

    # check if character can move left or right (if on bricks)
    def checkLeftRight(self, y):
        if y in listOfValidYAxisValues:
            return True
        else:
            return False

    # check if character is on top ladder
    def isTopLadder(self, y):
        if y == 2 or y == 1 or y == 0:
            return True
        else:
            return False



    # updates position of character
    def __update_position__(self, key):
        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()

        if key == Qt.Key_Escape:
            self.levelMusic.stop()
            from main_window import MainWindow
            self.mainMenu = MainWindow()
            self.close()

        if key == Qt.Key_D:
            if self.checkLeftRight(rec1.y()):
                if self.isTopLadder(rec1.y()):
                    if rec1.x() < 1160:
                        self.player1.playerLabel.setMovie(self.player1.playerRunRight)
                        self.player1.playerRunRight.start()
                        self.player1.updatePosition(rec1.x() + self.player1.korak, rec1.y())
                else:
                    if rec1.x() < 1825:
                        self.player1.playerLabel.setMovie(self.player1.playerRunRight)
                        self.player1.playerRunRight.start()
                        self.player1.updatePosition(rec1.x() + self.player1.korak, rec1.y())

                #if self.checkGorillaCollision(rec1.x(), rec1.y()):
                #   self.player1.updatePosition(100, 950)

        elif key == Qt.Key_S:
            if rec1.y() < 950:
                if self.checkLadderDown(rec1.x(), rec1.y()):
                    self.player1.playerLabel.setMovie(self.player1.playerClimb)
                    self.player1.playerClimb.start()
                    self.player1.updatePosition(rec1.x(), rec1.y() + self.player1.korak)
        elif key == Qt.Key_W:
            if rec1.y()<150 and self.player1.korak==20: # ako ostane korak 20 ode mnogo gore pa ne moze levo i desno
                self.player1.korak=10
            if self.checkLadderUp(rec1.x(), rec1.y()):
                self.player1.playerLabel.setMovie(self.player1.playerClimb)
                self.player1.playerClimb.start()
                self.player1.updatePosition(rec1.x(), rec1.y() - self.player1.korak)
        elif key == Qt.Key_A:
            if self.checkLeftRight(rec1.y()):
                if self.isTopLadder(rec1.y()):
                    if rec1.x() > 645:
                        self.player1.playerLabel.setMovie(self.player1.playerRunLeft)
                        self.player1.playerRunLeft.start()
                        self.player1.updatePosition(rec1.x() - self.player1.korak, rec1.y())
                else:
                    if rec1.x() > -5:
                        self.player1.playerLabel.setMovie(self.player1.playerRunLeft)
                        self.player1.playerRunLeft.start()
                        self.player1.updatePosition(rec1.x() - self.player1.korak, rec1.y())

                #if self.checkGorillaCollision(rec1.x(), rec1.y()):
                #    self.player1.updatePosition(100, 950)

        if key == Qt.Key_Right:
            if self.checkLeftRight(rec2.y()):
                if self.isTopLadder(rec2.y()):
                    if rec2.x() < 1160:
                        self.player2.playerLabel.setMovie(self.player2.playerRunRight)
                        self.player2.playerRunRight.start()
                        self.player2.updatePosition(rec2.x() + self.player2.korak, rec2.y())
                else:
                    if rec2.x() < 1825:
                        self.player2.playerLabel.setMovie(self.player2.playerRunRight)
                        self.player2.playerRunRight.start()
                        self.player2.updatePosition(rec2.x() + self.player2.korak, rec2.y())

                #if self.checkGorillaCollision(rec2.x(), rec2.y()):
                #    self.player2.updatePosition(1720, 950)

        elif key == Qt.Key_Down:
            if rec2.y() < 950:
                if self.checkLadderDown(rec2.x(), rec2.y()):
                    self.player2.playerLabel.setMovie(self.player2.playerClimb)
                    self.player2.playerClimb.start()
                    self.player2.updatePosition(rec2.x(), rec2.y() + self.player2.korak)
        elif key == Qt.Key_Up:
            if rec2.y() < 150 and self.player2.korak == 20:  # ako ostane korak 20 ode mnogo gore pa ne moze levo i desno
                self.player2.korak = 10
            if self.checkLadderUp(rec2.x(), rec2.y()):
                self.player2.playerLabel.setMovie(self.player2.playerClimb)
                self.player2.playerClimb.start()
                self.player2.updatePosition(rec2.x(), rec2.y() - self.player2.korak)
        elif key == Qt.Key_Left:
            if self.checkLeftRight(rec2.y()):
                if self.isTopLadder(rec2.y()):
                    if rec2.x() > 645:
                        self.player2.playerLabel.setMovie(self.player2.playerRunLeft)
                        self.player2.playerRunLeft.start()
                        self.player2.updatePosition(rec2.x() - self.player2.korak, rec2.y())
                else:
                    if rec2.x() > -5:
                        self.player2.playerLabel.setMovie(self.player2.playerRunLeft)
                        self.player2.playerRunLeft.start()
                        self.player2.updatePosition(rec2.x() - self.player2.korak, rec2.y())

                #if self.checkGorillaCollision(rec2.x(), rec2.y()):
                #    self.player2.updatePosition(1720, 950)


    def initCheckCollisions(self):
        self.checkCollisionSignal.connect(self.checkCollisions)
        self.collisionThread = Thread(target=self.checkCollisionThread)
        self.collisionThread.setDaemon(True)
        self.collisionThread.start()


    def checkCollisionThread(self):
        time.sleep(7)
        while 1:
            time.sleep(0.2)
            self.checkCollisionSignal.emit()

    def checkCollisions(self):
        if self.gorilla.gorillaLabel.x() <= self.player1.playerLabel.x() <= self.gorilla.gorillaLabel.x() + 100 or self.gorilla.gorillaLabel.x() <= self.player1.playerLabel.x() + 100 <= self.gorilla.gorillaLabel.x() + 100:
            if self.gorilla.gorillaLabel.y() <= self.player1.playerLabel.y() <= self.gorilla.gorillaLabel.y() + 100 or self.gorilla.gorillaLabel.y() <= self.player1.playerLabel.y() + 100 <= self.gorilla.gorillaLabel.y() + 100:
                self.player1.playerLives -= 1
                self.player1.livesLabel.setText(str(self.player1.playerLives))
                if self.player1.playerLives == 0:
                    self.player1.updatePosition(2500, 500)
                else:
                    self.player1.updatePosition(100, 950)

        if self.gorilla.gorillaLabel.x() <= self.player2.playerLabel.x() <= self.gorilla.gorillaLabel.x() + 100 or self.gorilla.gorillaLabel.x() <= self.player2.playerLabel.x() + 100 <= self.gorilla.gorillaLabel.x() + 100:
            if self.gorilla.gorillaLabel.y() <= self.player2.playerLabel.y() <= self.gorilla.gorillaLabel.y() + 100 or self.gorilla.gorillaLabel.y() <= self.player2.playerLabel.y() + 100 <= self.gorilla.gorillaLabel.y() + 100:
                self.player2.playerLives -= 1
                self.player2.livesLabel.setText(str(self.player2.playerLives))
                if self.player2.playerLives == 0:
                    self.player2.updatePosition(2500, 800)
                else:
                    self.player2.updatePosition(1720, 950)

        if self.gorilla.barrel1LabelCreated == 1:
            if self.gorilla.barrel1Label.x() <= self.player1.playerLabel.x() <= self.gorilla.barrel1Label.x() + 100 or self.gorilla.barrel1Label.x() <= self.player1.playerLabel.x() + 100 <= self.gorilla.barrel1Label.x() + 100:
                if self.gorilla.barrel1Label.y() <= self.player1.playerLabel.y() <= self.gorilla.barrel1Label.y() + 100 or self.gorilla.barrel1Label.y() <= self.player1.playerLabel.y() + 100 <= self.gorilla.barrel1Label.y() + 100:
                    self.player1.playerLives -= 1
                    self.player1.livesLabel.setText(str(self.player1.playerLives))
                    if self.player1.playerLives == 0:
                        self.player1.updatePosition(2500, 500)
                    else:
                        self.player1.updatePosition(100, 950)

            if self.gorilla.barrel1Label.x() <= self.player2.playerLabel.x() <= self.gorilla.barrel1Label.x() + 100 or self.gorilla.barrel1Label.x() <= self.player2.playerLabel.x() + 100 <= self.gorilla.barrel1Label.x() + 100:
                if self.gorilla.barrel1Label.y() <= self.player2.playerLabel.y() <= self.gorilla.barrel1Label.y() + 100 or self.gorilla.barrel1Label.y() <= self.player2.playerLabel.y() + 100 <= self.gorilla.barrel1Label.y() + 100:
                    self.player2.playerLives -= 1
                    self.player2.livesLabel.setText(str(self.player2.playerLives))
                    if self.player2.playerLives == 0:
                        self.player2.updatePosition(2500, 800)
                    else:
                        self.player2.updatePosition(1720, 950)

        if self.gorilla.barrel2LabelCreated == 1:
            if self.gorilla.barrel2Label.x() <= self.player1.playerLabel.x() <= self.gorilla.barrel2Label.x() + 100 or self.gorilla.barrel2Label.x() <= self.player1.playerLabel.x() + 100 <= self.gorilla.barrel2Label.x() + 100:
                if self.gorilla.barrel2Label.y() <= self.player1.playerLabel.y() <= self.gorilla.barrel2Label.y() + 100 or self.gorilla.barrel2Label.y() <= self.player1.playerLabel.y() + 100 <= self.gorilla.barrel2Label.y() + 100:
                    self.player1.playerLives -= 1
                    self.player1.livesLabel.setText(str(self.player1.playerLives))
                    if self.player1.playerLives == 0:
                        self.player1.updatePosition(2500, 500)
                    else:
                        self.player1.updatePosition(100, 950)

            if self.gorilla.barrel2Label.x() <= self.player2.playerLabel.x() <= self.gorilla.barrel2Label.x() + 100 or self.gorilla.barrel2Label.x() <= self.player2.playerLabel.x() + 100 <= self.gorilla.barrel2Label.x() + 100:
                if self.gorilla.barrel2Label.y() <= self.player2.playerLabel.y() <= self.gorilla.barrel2Label.y() + 100 or self.gorilla.barrel2Label.y() <= self.player2.playerLabel.y() + 100 <= self.gorilla.barrel2Label.y() + 100:
                    self.player2.playerLives -= 1
                    self.player2.livesLabel.setText(str(self.player2.playerLives))
                    if self.player2.playerLives == 0:
                        self.player2.updatePosition(2500, 800)
                    else:
                        self.player2.updatePosition(1720, 950)

        if self.gorilla.barrel3LabelCreated == 1:
            if self.gorilla.barrel3Label.x() <= self.player1.playerLabel.x() <= self.gorilla.barrel3Label.x() + 100 or self.gorilla.barrel3Label.x() <= self.player1.playerLabel.x() + 100 <= self.gorilla.barrel3Label.x() + 100:
                if self.gorilla.barrel3Label.y() <= self.player1.playerLabel.y() <= self.gorilla.barrel3Label.y() + 100 or self.gorilla.barrel3Label.y() <= self.player1.playerLabel.y() + 100 <= self.gorilla.barrel3Label.y() + 100:
                    self.player1.playerLives -= 1
                    self.player1.livesLabel.setText(str(self.player1.playerLives))
                    if self.player1.playerLives == 0:
                        self.player1.updatePosition(2500, 500)
                    else:
                        self.player1.updatePosition(100, 950)

            if self.gorilla.barrel3Label.x() <= self.player2.playerLabel.x() <= self.gorilla.barrel3Label.x() + 100 or self.gorilla.barrel3Label.x() <= self.player2.playerLabel.x() + 100 <= self.gorilla.barrel3Label.x() + 100:
                if self.gorilla.barrel3Label.y() <= self.player2.playerLabel.y() <= self.gorilla.barrel3Label.y() + 100 or self.gorilla.barrel3Label.y() <= self.player2.playerLabel.y() + 100 <= self.gorilla.barrel3Label.y() + 100:
                    self.player2.playerLives -= 1
                    self.player2.livesLabel.setText(str(self.player2.playerLives))
                    if self.player2.playerLives == 0:
                        self.player2.updatePosition(2500, 800)
                    else:
                        self.player2.updatePosition(1720, 950)

        if self.gorilla.barrel4LabelCreated == 1:
            if self.gorilla.barrel4Label.x() <= self.player1.playerLabel.x() <= self.gorilla.barrel4Label.x() + 100 or self.gorilla.barrel4Label.x() <= self.player1.playerLabel.x() + 100 <= self.gorilla.barrel4Label.x() + 100:
                if self.gorilla.barrel4Label.y() <= self.player1.playerLabel.y() <= self.gorilla.barrel4Label.y() + 100 or self.gorilla.barrel4Label.y() <= self.player1.playerLabel.y() + 100 <= self.gorilla.barrel4Label.y() + 100:
                    self.player1.playerLives -= 1
                    self.player1.livesLabel.setText(str(self.player1.playerLives))
                    if self.player1.playerLives == 0:
                        self.player1.updatePosition(2500, 500)
                    else:
                        self.player1.updatePosition(100, 950)

            if self.gorilla.barrel4Label.x() <= self.player2.playerLabel.x() <= self.gorilla.barrel4Label.x() + 100 or self.gorilla.barrel4Label.x() <= self.player2.playerLabel.x() + 100 <= self.gorilla.barrel4Label.x() + 100:
                if self.gorilla.barrel4Label.y() <= self.player2.playerLabel.y() <= self.gorilla.barrel4Label.y() + 100 or self.gorilla.barrel4Label.y() <= self.player2.playerLabel.y() + 100 <= self.gorilla.barrel4Label.y() + 100:
                    self.player2.playerLives -= 1
                    self.player2.livesLabel.setText(str(self.player2.playerLives))
                    if self.player2.playerLives == 0:
                        self.player2.updatePosition(2500, 800)
                    else:
                        self.player2.updatePosition(1720, 950)

        if self.gorilla.barrel5LabelCreated == 1:
            if self.gorilla.barrel5Label.x() <= self.player1.playerLabel.x() <= self.gorilla.barrel5Label.x() + 100 or self.gorilla.barrel5Label.x() <= self.player1.playerLabel.x() + 100 <= self.gorilla.barrel5Label.x() + 100:
                if self.gorilla.barrel5Label.y() <= self.player1.playerLabel.y() <= self.gorilla.barrel5Label.y() + 100 or self.gorilla.barrel5Label.y() <= self.player1.playerLabel.y() + 100 <= self.gorilla.barrel5Label.y() + 100:
                    self.player1.playerLives -= 1
                    self.player1.livesLabel.setText(str(self.player1.playerLives))
                    if self.player1.playerLives == 0:
                        self.player1.updatePosition(2500, 500)
                    else:
                        self.player1.updatePosition(100, 950)
            if self.gorilla.barrel5Label.x() <= self.player2.playerLabel.x() <= self.gorilla.barrel5Label.x() + 100 or self.gorilla.barrel5Label.x() <= self.player2.playerLabel.x() + 100 <= self.gorilla.barrel5Label.x() + 100:
                if self.gorilla.barrel5Label.y() <= self.player2.playerLabel.y() <= self.gorilla.barrel5Label.y() + 100 or self.gorilla.barrel5Label.y() <= self.player2.playerLabel.y() + 100 <= self.gorilla.barrel5Label.y() + 100:
                     self.player2.playerLives -= 1
                     self.player2.livesLabel.setText(str(self.player2.playerLives))
                     if self.player2.playerLives == 0:
                        self.player2.updatePosition(2500, 800)
                     else:
                        self.player2.updatePosition(1720, 950)


    def closeEvent(self, event):
        self.key_notifier.die()

    def exitLevel(self):
        self.levelMusic.stop()
        self.close()
