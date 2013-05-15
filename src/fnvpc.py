#!/usr/bin/env python

# Fallout NV Pip Colorizer
# by Nicholas "Lavacano" O'Connor
# Purpose: Generate a PipBoy color string for use in Fallout NV (and FO3)

# TODO: Get the config saving working

# Espanol: Todos comentarios son en ingles, lo siento!

import sip
sip.setapi("QString", 2)

import sys, os

from PyQt4 import QtCore, QtGui, uic

qapp = QtGui.QApplication(sys.argv)
winicon = QtGui.QIcon("paint.png")
qapp.setWindowIcon(winicon)

class lang():
    """Only here for scope reasons"""
    
    def __init__(self):
        # Doesn't actually do anything other than store stuff
        self.language = ""
        self.langset = False
        self.mainUi = ""
        self.writeUi = ""

langcfg = lang()

# I'm going to use these variables once then forget about them.
cfg_game = ""
cfg_color = ""

def startTheApp():
    if langcfg.language == "en":
        langcfg.mainUi = "fnvpc.ui"
        langcfg.writeUi = "writeini.ui"
    elif langcfg.language == "es":
        langcfg.mainUi = "fnvpc_es.ui"
        langcfg.writeUi = "writeini_es.ui"
    #oldwindow = QtGui.QDialog()

    #class AppWindow(QtGui.QDialog): # whoo subclassing
    #    def closeEvent(self, event):
    #        with open("fnvpc-new.cfg", "w") as newCFG:
    #            print "Writing config"
    #            if writewinui.hud.isChecked():
    #                newCFG.write("piporhud=hud\n")
    #            elif writewinui.pipboy.isChecked():
    #                newCFG.write("piporhud=pip\n")
    #            else: # Hey you never know
    #                newCFG.write("piporhud=unset\n")
    #            if writewinui.fallout3.isChecked():
    #                newCFG.write("game=fo3\n")
    #            elif writewinui.falloutnv.isChecked():
    #                newCFG.write("game=fonv\n")
    #            else: # You STILL never know
    #                newCFG.write("game=unset\n")
    #            newCFG.write("lang=" + langcfg.language)

    #window = AppWindow(oldwindow)
    window = QtGui.QDialog()
    winui = uic.loadUi(langcfg.mainUi, window)

    # Picker button
    pickerIcon = QtGui.QIcon("color_wheel.png")
    winui.picker.setIcon(pickerIcon)

    def pickAColor(Bool=None):
        colorDialog = QtGui.QColorDialog()
        chosenColor = colorDialog.getColor()

        winui.desiredColor.setText(chosenColor.name().strip("#"))

    winui.picker.pyqtConfigure(clicked=pickAColor)

    # Convert button
    convertIcon = QtGui.QIcon("convert.png")
    winui.convert.setIcon(convertIcon)

    def convertTheColor(Bool=None):
        desiredColor = winui.desiredColor.text().lower() + "ff"
        returnedColor = int(desiredColor, 16)

        winui.falloutColor.setText(str(returnedColor).strip("L"))

    winui.convert.pyqtConfigure(clicked=convertTheColor)

    writewin = QtGui.QDialog()
    writewinui = uic.loadUi(langcfg.writeUi, writewin)

    if cfg_game == "fo3":
        writewinui.fallout3.pyqtConfigure(checked=True)
    elif cfg_game == "fonv":
        writewinui.falloutnv.pyqtConfigure(checked=True)

    if cfg_color == "pip":
        writewinui.pipboy.pyqtConfigure(checked=True)
    elif cfg_color == "hud":
        writewinui.hud.pyqtConfigure(checked=True)

    def readTheIniFile(Bool=None):
        if writewinui.falloutnv.isChecked():
            iniDir = os.environ["USERPROFILE"] + "\\My Documents\\My Games\\FalloutNV"
        elif writewinui.fallout3.isChecked():
            iniDir = os.environ["USERPROFILE"] + "\\My Documents\\My Games\\Fallout3"

        iniFile = open(iniDir + "\\FalloutPrefs.ini")

        if writewinui.hud.isChecked():
            checkFor = "uHUD" # I'd rather check the whole string, but that would
                              # require splitting because the two settings have
                              # different name lengths, and since not all lines have
                              # something to split on, checking the first four chars
                              # will have to do.
        elif writewinui.pipboy.isChecked():
            checkFor = "uPip"

        for line in iniFile:
            if line[:4] == checkFor:
                results = line.split("=")
                winui.falloutColor.setText(results[1].strip())
                resultCol = hex(int(results[1].strip()))
                winui.desiredColor.setText(resultCol[2:8])
        iniFile.close()

    writewinui.readbtn.pyqtConfigure(clicked=readTheIniFile)

    def writeTheIniFile(Bool=None):
        if writewinui.falloutnv.isChecked():
            iniDir = os.environ["USERPROFILE"] + "\\My Documents\\My Games\\FalloutNV"
        elif writewinui.fallout3.isChecked():
            iniDir = os.environ["USERPROFILE"] + "\\My Documents\\My Games\\Fallout3"

        iniFile = open(iniDir + "\\FalloutPrefs.ini")
        newiniFile = open(iniDir + "\\FalloutPrefs-NEW.ini", "w")

        if writewinui.hud.isChecked():
            checkFor = "uHUD" # I'd rather check the whole string, but that would
                              # require splitting because the two settings have
                              # different name lengths, and since not all lines have
                              # something to split on, checking the first four chars
                              # will have to do.
        elif writewinui.pipboy.isChecked():
            checkFor = "uPip"

        for line in iniFile:
            if line[:4] == checkFor:
                if checkFor == "uPip":
                    newiniFile.write("uPipboyColor=" + winui.falloutColor.text() + "\n")
                elif checkFor == "uHUD":
                    newiniFile.write("uHUDColor=" + winui.falloutColor.text() + "\n")
            else:
                newiniFile.write(line)

        iniFile.close()
        newiniFile.close()

        os.remove(iniDir + "\\FalloutPrefs.ini")
        os.rename(iniDir + "\\FalloutPrefs-NEW.ini", iniDir + "\\FalloutPrefs.ini")

    writewinui.writebtn.pyqtConfigure(clicked=writeTheIniFile)

    def opentheWriter(Bool=None):
        writewin.show()
    winui.write.pyqtConfigure(clicked=opentheWriter)

    # This is apparently better because then I can intercept the quit signal
    winui.connect(winui.gtfo, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT('quit()'))

    window.show()

with open("fnvpc.cfg") as cfgfile:
    for line in cfgfile:
        cfg = line.strip().split("=")
        if cfg[0] == "lang":
            if cfg[1] == "unset": # Select Language
                langwin = QtGui.QDialog()
                langui = uic.loadUi("language.ui", langwin)

                langcfg.langSet = False
                def langEn(Bool=None):
                    """English button"""
                    langcfg.langSet = True
                    langcfg.language = "en"
                    langwin.hide()
                    startTheApp()
                langui.english.pyqtConfigure(clicked=langEn)
                def langEs(Bool=None):
                    """Spanish button"""
                    langcfg.langSet = True
                    langcfg.language = "es"
                    langwin.hide()
                    startTheApp()
                langui.espanol.pyqtConfigure(clicked=langEs)
                langwin.show()
            else:
                langcfg.language = cfg[1]
                startTheApp()
        elif cfg[0] == "piporhud":
            cfg_color = cfg[1]
        elif cfg[0] == "game":
            cfg_game = cfg[1]

sys.exit(qapp.exec_())