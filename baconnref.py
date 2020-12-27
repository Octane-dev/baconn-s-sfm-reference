import sys

sys.path.insert(0, "C:\Program Files (x86)\Steam\steamapps\common\SourceFilmmaker\game\sdktools\python\2.7\win32\Lib\site-packages\vs")
sys.path.insert(0, "C:\Program Files (x86)\Steam\steamapps\common\SourceFilmmaker\game\sdktools\python\global\lib\site-packages\sfm")

#Written by https://steamcommunity.com/id/theziker/ 26/12/2020

import sfmApp
import vs
import sfm
import types
import os, ast
from PySide import QtGui, QtCore
from PySide.phonon import Phonon

# ------------- window --------------- #

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.media = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(400, 400)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)

    # ------------- create buttons n shit --------------- #
        
        self.Browse = QtGui.QPushButton("...")
        self.PauseButt = QtGui.QPushButton("Pause")
        self.Play = QtGui.QPushButton("Play")
        self.slider = Phonon.SeekSlider(self.media)

    # ------------- layout --------------- #
        
        self.slider.setFixedHeight(8)
        self.slider.setSingleStep(36)
        layout = QtGui.QGridLayout(self)
        vbox = QtGui.QVBoxLayout()
        layout.addWidget(self.video, 0, 0, 1, 3)
        layout.addWidget(self.Browse, 2, 2)
        layout.addWidget(self.slider, 2, 0, 1, 2)
        layout.addWidget(self.PauseButt, 1, 0)
        layout.addWidget(self.Play, 1, 1)
        layout.setRowStretch(0, 1)

    # ------------- connecting functions --------------- #
        
        self.media.stateChanged.connect(self.handleStateChanged)
        self.Browse.clicked.connect(self.handleButtonChoose)
        self.PauseButt.clicked.connect(self.handleButtonPause)
        self.Play.clicked.connect(self.handleButtonPlay)

    # ------------- defining functions --------------- #

#import media

    def handleButtonChoose(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
            dialog = QtGui.QFileDialog(self)
            dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
            if dialog.exec_() == QtGui.QDialog.Accepted:
                path = dialog.selectedFiles()[0]
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.media.play()
            dialog.deleteLater()
        else:
            dialog = QtGui.QFileDialog(self)
            dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
            if dialog.exec_() == QtGui.QDialog.Accepted:
                path = dialog.selectedFiles()[0]
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.media.play()
            dialog.deleteLater()


    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.Browse.setText("...")
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.Browse.setText("...")
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print ("ERROR: could not play: %s" % source)
                print ("  %s" % self.media.errorString())

#pause

    def handleButtonPause(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.pause()

#play

    def handleButtonPlay(self):
        if self.media.state() == Phonon.PausedState:
            self.media.play()

#create sfm window

exampleWindow = Window()
sfmApp.RegisterTabWindow( "Window", "Third Viewport", shiboken.getCppPointer( exampleWindow ) [0] )
sfm.App.ShowTabWindow("ThirdView")

#if __name__ == '__main__':
#
#    import sys
#    app = QtGui.QApplication(sys.argv)
#    app.setApplicationName("MediaPlayer")
#    window = Window()
#    window.show()
#    sys.exit(app.exec_())
