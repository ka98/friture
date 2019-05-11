
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QStyle

__colorThemesInstance = None

def ColorThemes(app = None):
    global __colorThemesInstance
    if __colorThemesInstance is None:
       __colorThemesInstance = __ColorThemes(app)
    return __colorThemesInstance

class __ColorThemes:

    window = None
    windowText = None
    disabledWindowText = None
    base = None
    alternativeBase = None
    toolTipBase = None
    toolTipText = None
    text = None
    disabledText = None
    dark = None
    shadow = None
    button = None
    buttonText = None
    disabledButtonText = None
    brightText = None
    link = None
    highlight = None
    disabledHighlight = None
    highlightedText = None
    disabledHighlighttedText = None

    curve1 = None
    curve2 = None
    chartBackgroundUpperGradient1 = None
    chartBackgroundLowerGradient1 = None
    chartBackgroundUpperGradient2 = None
    chartBackgroundLowerGradient2 = None
    statisticsWindow = None
    ruler = None
    octaveLabelText = None
    gridStrong = None
    gridWeak = None
    octavePeakHistroy = None
    darken = None

    app = None

    def __init__(self, app):
        self.app = app

    def changeToLightTheme(self):
        palette = QApplication.style().standardPalette()

        self.window = palette.color(QPalette.Window)
        self.windowText = palette.color(QPalette.WindowText)
        self.disabledWindowText = palette.color(QPalette.Disabled, QPalette.WindowText)
        self.base = palette.color(QPalette.Base)
        self.alternativeBase = palette.color(QPalette.AlternateBase)
        self.toolTipBase = palette.color(QPalette.ToolTipBase)
        self.toolTipText = palette.color(QPalette.ToolTipText)
        self.text = palette.color(QPalette.Text)
        self.disabledText = palette.color(QPalette.Disabled, QPalette.Text)
        self.dark = palette.color(QPalette.Dark)
        self.shadow = palette.color(QPalette.Shadow)
        self.button = palette.color(QPalette.Button)
        self.buttonText = palette.color(QPalette.ButtonText)
        self.disabledButtonText = palette.color(QPalette.Disabled, QPalette.ButtonText)
        self.brightText = palette.color(QPalette.BrightText)
        self.link = palette.color(QPalette.Link)
        self.highlight = palette.color(QPalette.Highlight)
        self.disabledHighlight = palette.color(QPalette.Disabled, QPalette.Highlight)
        self.highlightedText = palette.color(QPalette.HighlightedText)
        self.disabledHighlighttedText = palette.color(QPalette.Disabled, QPalette.HighlightedText)

        self.curve1 = QColor(255,0,0)
        self.curve1 = QColor(0,0,255)
        self.chartBackgroundUpperGradient1 = QColor("#E0E0E0")
        self.chartBackgroundLowerGradient1 = QColor("#FFFFFF")
        self.chartBackgroundUpperGradient2 = 0.85
        self.chartBackgroundLowerGradient2 = 1
        self.ruler = QColor(0,0,0)
        self.statisticsWindow = "white"
        self.octaveLabelText = QColor(0,0,0)
        self.gridStrong = QColor(Qt.gray)
        self.gridWeak = QColor(Qt.lightGray)
        self.octavePeakHistroy = [QColor(255, gb, gb) for gb in range(0, 256)]
        self.darken = False

    def changeToDarkTheme(self):
        self.window = QColor(53, 53, 53)
        self.windowText = QColor(255,255,255)
        self.disabledWindowText = QColor(127, 127, 127)
        self.base = QColor(42, 42, 42)
        self.alternativeBase = QColor(66, 66, 66)
        self.toolTipBase = QColor(255,255,255)
        self.toolTipText = QColor(255,255,255)
        self.text = QColor(255,255,255)
        self.disabled = QColor(127, 127, 127)
        self.dark = QColor(35, 35, 35)
        self.shadow = QColor(20, 20, 20)
        self.button = QColor(20, 20, 20)
        self.buttonText = QColor(255,255,255)
        self.disabledButtonText = QColor(127, 127, 127)
        self.brightText = QColor(255,0,0)
        self.link = QColor(42, 13, 218)
        self.highlight = QColor(42, 130, 218)
        self.disabledHighlight = QColor(80, 80, 80)
        self.highlightedText = QColor(255,255,255)
        self.disabledHighlighttedText = QColor(127, 127, 127)

        self.curve1 = QColor(255,255,255)
        self.curve2 = QColor(255,80,80)
        self.chartBackgroundUpperGradient1 = QColor("#000000")
        self.chartBackgroundLowerGradient1 = QColor("#000000")
        self.chartBackgroundUpperGradient2 = 0.
        self.chartBackgroundLowerGradient2 = 0.
        self.ruler = QColor(255,255,255)
        self.statisticsWindow = "black"
        self.octaveLabelText = QColor(255,255,255)
        self.gridStrong = QColor(50,50,50)
        self.gridWeak = QColor(35,35,35)
        self.octavePeakHistroy = [QColor(gb + 30, 0, 0) for gb in range(0, 255)]
        self.darken = True

    def setPalette(self):
        palette = QPalette()

        palette.setColor(QPalette.Window, self.window)
        palette.setColor(QPalette.WindowText, self.windowText)
        palette.setColor(QPalette.Disabled, QPalette.WindowText, self.disabledWindowText)
        palette.setColor(QPalette.Base, self.base)
        palette.setColor(QPalette.AlternateBase, self.alternativeBase)
        palette.setColor(QPalette.ToolTipBase, self.toolTipBase)
        palette.setColor(QPalette.ToolTipText, self.toolTipText)
        palette.setColor(QPalette.Text, self.text)
        palette.setColor(QPalette.Disabled, QPalette.Text, self.disabledText)
        palette.setColor(QPalette.Dark, self.dark)
        palette.setColor(QPalette.Shadow, self.shadow)
        palette.setColor(QPalette.Button, self.button)
        palette.setColor(QPalette.ButtonText, self.buttonText)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, self.disabledButtonText)
        palette.setColor(QPalette.BrightText, self.brightText)
        palette.setColor(QPalette.Link, self.link)
        palette.setColor(QPalette.Highlight, self.highlight)
        palette.setColor(QPalette.Disabled, QPalette.Highlight, self.disabledHighlight)
        palette.setColor(QPalette.HighlightedText, self.highlightedText)
        palette.setColor(QPalette.Disabled, QPalette.HighlightedText, self.disabledHighlighttedText)

        # App has to be restarted in order to change

        self.app.setPalette(palette)


