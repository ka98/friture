#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timothée Lecomte

# This file is part of Friture.
#
# Friture is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# Friture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Friture.  If not, see <http://www.gnu.org/licenses/>.

import sys
import logging

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication

from colorThemes import ColorThemes
from friture.audiobackend import AudioBackend
from friture.ui_settings import Ui_Settings_Dialog

no_input_device_title = "No audio input device found"

no_input_device_message = """No audio input device has been found.

Friture needs at least one input device. Please check your audio configuration.

Friture will now exit.
"""


class Settings_Dialog(QtWidgets.QDialog, Ui_Settings_Dialog):

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_Settings_Dialog.__init__(self)

        self.logger = logging.getLogger(__name__)

        # Setup the user interface
        self.setupUi(self)

        devices = AudioBackend().get_readable_devices_list()

        if devices == []:
            # no audio input device: display a message and exit
            QtWidgets.QMessageBox.critical(self, no_input_device_title, no_input_device_message)
            QtCore.QTimer.singleShot(0, self.exitOnInit)
            sys.exit(1)
            return

        for device in devices:
            self.comboBox_inputDevice.addItem(device)

        channels = AudioBackend().get_readable_current_channels()
        for channel in channels:
            self.comboBox_firstChannel.addItem(channel)
            self.comboBox_secondChannel.addItem(channel)

        themes = ["light", "dark"]
        self.comboBox_applicationTheme.addItems(themes)

        current_device = AudioBackend().get_readable_current_device()
        self.comboBox_inputDevice.setCurrentIndex(current_device)

        first_channel = AudioBackend().get_current_first_channel()
        self.comboBox_firstChannel.setCurrentIndex(first_channel)
        second_channel = AudioBackend().get_current_second_channel()
        self.comboBox_secondChannel.setCurrentIndex(second_channel)

        self.comboBox_applicationTheme.setCurrentIndex(0)

        # signals
        self.comboBox_inputDevice.currentIndexChanged.connect(self.input_device_changed)
        self.comboBox_firstChannel.activated.connect(self.first_channel_changed)
        self.comboBox_secondChannel.activated.connect(self.second_channel_changed)
        self.radioButton_single.toggled.connect(self.single_input_type_selected)
        self.radioButton_duo.toggled.connect(self.duo_input_type_selected)

    # slot
    # used when no audio input device has been found, to exit immediately
    def exitOnInit(self):
        QtWidgets.QApplication.instance().quit()

    # slot
    def input_device_changed(self, index):
        self.parent().ui.actionStart.setChecked(False)

        success, index = AudioBackend().select_input_device(index)

        self.comboBox_inputDevice.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage("Impossible to use the selected input device, reverting to the previous one")

        # reset the channels
        channels = AudioBackend().get_readable_current_channels()

        self.comboBox_firstChannel.clear()
        self.comboBox_secondChannel.clear()

        for channel in channels:
            self.comboBox_firstChannel.addItem(channel)
            self.comboBox_secondChannel.addItem(channel)

        first_channel = AudioBackend().get_current_first_channel()
        self.comboBox_firstChannel.setCurrentIndex(first_channel)
        second_channel = AudioBackend().get_current_second_channel()
        self.comboBox_secondChannel.setCurrentIndex(second_channel)

        self.parent().ui.actionStart.setChecked(True)

    # slot
    def first_channel_changed(self, index):
        self.parent().ui.actionStart.setChecked(False)

        success, index = AudioBackend().select_first_channel(index)

        self.comboBox_firstChannel.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage("Impossible to use the selected channel as the first channel, reverting to the previous one")

        self.parent().ui.actionStart.setChecked(True)

    # slot
    def second_channel_changed(self, index):
        self.parent().ui.actionStart.setChecked(False)

        success, index = AudioBackend().select_second_channel(index)

        self.comboBox_secondChannel.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage("Impossible to use the selected channel as the second channel, reverting to the previous one")

        self.parent().ui.actionStart.setChecked(True)

    # slot
    def single_input_type_selected(self, checked):
        if checked:
            self.groupBox_second.setEnabled(False)
            AudioBackend().set_single_input()
            self.logger.info("Switching to single input")

    # slot
    def duo_input_type_selected(self, checked):
        if checked:
            self.groupBox_second.setEnabled(True)
            AudioBackend().set_duo_input()
            self.logger.info("Switching to difference between two inputs")

    def application_theme_changed(self, index):
        #All the crazy shit in here
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowTitle("Restart needed")
        messageBox.setText("The application has to be restarted in order to apply the changes")
        messageBox.exec()

        if (index == 0):
            ColorThemes().changeToLightTheme()
        else :
            ColorThemes().changeToDarkTheme()

        self.parent().close()


    # method
    def saveState(self, settings):
        # for the input device, we search by name instead of index, since
        # we do not know if the device order stays the same between sessions
        settings.setValue("deviceName", self.comboBox_inputDevice.currentText())
        settings.setValue("firstChannel", self.comboBox_firstChannel.currentIndex())
        settings.setValue("secondChannel", self.comboBox_secondChannel.currentIndex())
        settings.setValue("duoInput", self.inputTypeButtonGroup.checkedId())
        settings.setValue("applicationTheme", self.comboBox_applicationTheme.currentIndex())

        settings.setValue("window", ColorThemes().window)
        settings.setValue("windowText", ColorThemes().windowText)
        settings.setValue("disabledWindowText", ColorThemes().disabledWindowText)
        settings.setValue("base", ColorThemes().base)
        settings.setValue("alternativeBase", ColorThemes().alternativeBase)
        settings.setValue("toolTipBase", ColorThemes().toolTipBase)
        settings.setValue("toolTipText", ColorThemes().toolTipText)
        settings.setValue("text", ColorThemes().text)
        settings.setValue("disabledText", ColorThemes().disabledText )
        settings.setValue("dark", ColorThemes().dark)
        settings.setValue("shadow", ColorThemes().shadow)
        settings.setValue("button", ColorThemes().button)
        settings.setValue("buttonText", ColorThemes().buttonText)
        settings.setValue("disabledButtonText", ColorThemes().disabledButtonText )
        settings.setValue("brightText", ColorThemes().brightText)
        settings.setValue("link", ColorThemes().link)
        settings.setValue("highlight", ColorThemes().highlight )
        settings.setValue("disabledHighlight", ColorThemes().disabledHighlight)
        settings.setValue("highlightedText", ColorThemes().highlightedText)
        settings.setValue("disabledHighlighttedText", ColorThemes().disabledHighlighttedText)

        settings.setValue("curve1", ColorThemes().curve1)
        settings.setValue("curve2", ColorThemes().curve2)
        settings.setValue("chartBackgroundUpperGradient1", ColorThemes().chartBackgroundUpperGradient1)
        settings.setValue("chartBackgroundLowerGradient1", ColorThemes().chartBackgroundLowerGradient1)
        settings.setValue("chartBackgroundUpperGradient2", ColorThemes().chartBackgroundUpperGradient2)
        settings.setValue("chartBackgroundLowerGradient2", ColorThemes().chartBackgroundLowerGradient2)
        settings.setValue("statisticsWindow", ColorThemes().statisticsWindow)
        settings.setValue("ruler", ColorThemes().ruler)
        settings.setValue("octaveLabelText", ColorThemes().octaveLabelText)
        settings.setValue("gridStrong", ColorThemes().gridStrong)
        settings.setValue("gridWeak", ColorThemes().gridWeak)
        settings.setValue("octavePeakHistroy", ColorThemes().octavePeakHistroy)
        settings.setValue("darken", ColorThemes().darken)

    # method
    def restoreState(self, settings):
        device_name = settings.value("deviceName", "")
        device_index = self.comboBox_inputDevice.findText(device_name)
        # change the device only if it exists in the device list
        if device_index >= 0:
            self.comboBox_inputDevice.setCurrentIndex(device_index)
            channel = settings.value("firstChannel", 0, type=int)
            self.comboBox_firstChannel.setCurrentIndex(channel)
            channel = settings.value("secondChannel", 0, type=int)
            self.comboBox_secondChannel.setCurrentIndex(channel)
            duo_input_id = settings.value("duoInput", 0, type=int)
            self.inputTypeButtonGroup.button(duo_input_id).setChecked(True)
        self.comboBox_applicationTheme.setCurrentIndex(settings.value("applicationTheme", 0, type=int))
        self.comboBox_applicationTheme.currentIndexChanged.connect(self.application_theme_changed) # listen to changes after tbe inital value is set

        palette = QApplication.style().standardPalette()

        ColorThemes().window = settings.value("window", palette.color(QPalette.Window))
        ColorThemes().windowText = settings.value("windowText", palette.color(QPalette.WindowText))
        ColorThemes().disabledWindowText = settings.value("disabledWindowText", palette.color(QPalette.Disabled, QPalette.WindowText))
        ColorThemes().base = settings.value("base", palette.color(QPalette.Base))
        ColorThemes().alternativeBase = settings.value("alternativeBase", palette.color(QPalette.AlternateBase))
        ColorThemes().toolTipBase = settings.value("toolTipBase", palette.color(QPalette.ToolTipBase))
        ColorThemes().toolTipText = settings.value("toolTipText", palette.color(QPalette.ToolTipText))
        ColorThemes().text = settings.value("text", palette.color(QPalette.Text))
        ColorThemes().disabledText = settings.value("disabledText", palette.color(QPalette.Disabled, QPalette.Text))
        ColorThemes().dark = palette.color(QPalette.Dark)
        ColorThemes().shadow = settings.value("shadow", palette.color(QPalette.Shadow))
        ColorThemes().button = settings.value("button", palette.color(QPalette.Button))
        ColorThemes().buttonText = settings.value("buttonText", palette.color(QPalette.ButtonText))
        ColorThemes().disabledButtonText = settings.value("disabledButtonText", palette.color(QPalette.Disabled, QPalette.ButtonText))
        ColorThemes().brightText = settings.value("brightText", palette.color(QPalette.BrightText))
        ColorThemes().link = settings.value("link", palette.color(QPalette.Link))
        ColorThemes().highlight = settings.value("highlight", palette.color(QPalette.Highlight))
        ColorThemes().disabledHighlight = settings.value("disabledHighlight", palette.color(QPalette.Disabled, QPalette.Highlight))
        ColorThemes().highlightedText = settings.value("highlightedText", palette.color(QPalette.HighlightedText))
        ColorThemes().disabledHighlighttedText = settings.value("disabledHighlighttedText", palette.color(QPalette.Disabled, QPalette.HighlightedText))

        ColorThemes().curve2 = settings.value("curve2", QColor(255,0,0))
        ColorThemes().curve1 = settings.value("curve1", QColor(0,0,255))
        ColorThemes().chartBackgroundUpperGradient1 = settings.value("chartBackgroundUpperGradient1", QColor("#E0E0E0"))
        ColorThemes().chartBackgroundLowerGradient1 = settings.value("chartBackgroundLowerGradient1", QColor("#FFFFFF"))
        ColorThemes().chartBackgroundUpperGradient2 = settings.value("chartBackgroundUpperGradient2", 0., type=float)
        ColorThemes().chartBackgroundLowerGradient2 = settings.value("chartBackgroundLowerGradient2", 0., type=float)
        ColorThemes().statisticsWindow = settings.value("statisticsWindow", "white")
        ColorThemes().ruler = settings.value("ruler", QColor(0,0,0))
        ColorThemes().octaveLabelText = settings.value("octaveLabelText", QColor(0,0,0))
        ColorThemes().gridStrong = settings.value("gridStrong", QColor(Qt.gray))
        ColorThemes().gridWeak = settings.value("gridWeak", QColor(Qt.lightGray))
        ColorThemes().octavePeakHistroy = settings.value("octavePeakHistroy", [QColor(255, gb, gb) for gb in range(0, 256)])
        ColorThemes().darken = settings.value("darken", False, type=bool)

        ColorThemes().setPalette()