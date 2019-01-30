from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint, QRect
import sys
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        icon = "icons/icon.png"
        self.setWindowTitle("Paint")
        self.setWindowIcon(QIcon(icon))
        self.setGeometry(400, 400, 800, 600)
        self.img = QImage(self.size(), QImage.Format_RGB32)
        self.img.fill(Qt.white)
        self.dr = False
        self.brSize = 2
        self.brColor = Qt.black
        self.lastPoint = QPoint()
        self.point_history = []
        self.events_history = [] #point_histor_events

        self.draw_modes = ['pen', 'polygon', 'erase']
        self.draw_mode = self.draw_modes[0]

        menu = self.menuBar()
        fmenu = menu.addMenu("File")
        brmenu = menu.addMenu("Размер кисти")
        brcolormenu = menu.addMenu("Цвет кисти")
        editMenu = menu.addMenu("Редактирование")
        save = QAction(QIcon("icons/save.png"), "Сохранить", self)
        save.setShortcut("Ctrl+S")
        fmenu.addAction(save)
        save.triggered.connect(self.save)
        #extendedMenu = menu.addMenu("Расширенные настрокйки")

        clear = QAction(QIcon("icons/clear.svg"), "Очистить", self)
        clear.setShortcut("C")
        fmenu.addAction(clear)
        clear.triggered.connect(self.clear)

        s1 = QAction(QIcon("icons/1.svg"), "1px", self)
        s1.setShortcut("Ctrl+1")
        brmenu.addAction(s1)

        s2 = QAction(QIcon("icons/2.svg"), "2px", self)
        s2.setShortcut("Ctrl+2")
        brmenu.addAction(s2)

        s3 = QAction(QIcon("icons/3.svg"), "3px", self)
        s3.setShortcut("Ctrl+3")
        brmenu.addAction(s3)

        s4 = QAction(QIcon("icons/4.svg"), "4px", self)
        s4.setShortcut("Ctrl+4")
        brmenu.addAction(s4)

        s5 = QAction(QIcon("icons/5.svg"), "5px", self)
        s5.setShortcut("Ctrl+5")
        brmenu.addAction(s5)

        s6 = QAction(QIcon("icons/6.svg"), "6px", self)
        s6.setShortcut("Ctrl+6")
        brmenu.addAction(s6)

        s7 = QAction(QIcon("icons/7.svg"), "7px", self)
        s7.setShortcut("Ctrl+7")
        brmenu.addAction(s7)

        s8 = QAction(QIcon("icons/8.svg"), "8px", self)
        s8.setShortcut("Ctrl+8")
        brmenu.addAction(s8)

        s9 = QAction(QIcon("icons/9.svg"), "9px", self)
        s9.setShortcut("Ctrl+9")
        brmenu.addAction(s9)

        s10 = QAction(QIcon("icons/10.svg"), "10px", self)
        s10.setShortcut("Ctrl+0")
        brmenu.addAction(s10)

        s1.triggered.connect(self.onePx)
        s2.triggered.connect(self.twoPx)
        s3.triggered.connect(self.threePx)
        s4.triggered.connect(self.fourPx)
        s5.triggered.connect(self.fivePx)
        s6.triggered.connect(self.sixPx)
        s7.triggered.connect(self.sevenPx)
        s8.triggered.connect(self.eightPx)
        s9.triggered.connect(self.ninePx)
        s10.triggered.connect(self.tenPx)

        cBlack = QAction(QIcon("icons/black.svg"), "Чёрный", self)
        brcolormenu.addAction(cBlack)

        cBlue = QAction(QIcon("icons/blue.jpg"), "Синий", self)
        brcolormenu.addAction(cBlue)

        cGreen = QAction(QIcon("icons/green.png"), "Зелёный", self)
        brcolormenu.addAction(cGreen)

        cRed = QAction(QIcon("icons/red.jpg"), "Красный", self)
        brcolormenu.addAction(cRed)

        cLightBl = QAction(QIcon("icons/lightblue.png"), "Голубой", self)
        brcolormenu.addAction(cLightBl)

        cPink = QAction(QIcon("icons/pink.jpg"), "Розовый", self)
        brcolormenu.addAction(cPink)

        cYellow = QAction(QIcon("icons/yellow.jpg"), "Жёлтый", self)
        brcolormenu.addAction(cYellow)

        cPurple = QAction(QIcon("icons/purple.png"), "Фиолетовый", self)
        brcolormenu.addAction(cPurple)

        cBrown = QAction(QIcon("icons/brown.png"), "Коричневый", self)
        brcolormenu.addAction(cBrown)

        cGray = QAction(QIcon("icons/gray.jpg"), "Серый", self)
        brcolormenu.addAction(cGray)

        backAction = QAction(QIcon("icons/back.png"), "Назад", self)
        backAction.setShortcut("Ctrl+Z")
        editMenu.addAction(backAction)
        forwardAction = QAction(QIcon("icons/forward.jpg"), "Вперёд", self)
        forwardAction.setShortcut("Ctrl+Y")
        editMenu.addAction(forwardAction)
        eraseAction = QAction(QIcon("icons/eraser.png"), "ластик", self)
        editMenu.addAction(eraseAction)
        self.show()
        eraseAction.triggered.connect(self.erase)
        forwardAction.triggered.connect(self.forward_event)
        backAction.triggered.connect(self.back_event)
        cBlack.triggered.connect(self.Black)
        cRed.triggered.connect(self.Red)
        cGreen.triggered.connect(self.Green)
        cBlue.triggered.connect(self.Blue)
        cLightBl.triggered.connect(self.LightBlue)
        cPink.triggered.connect(self.Pink)
        cYellow.triggered.connect(self.Yellow)
        cPurple.triggered.connect(self.Purple)
        cBrown.triggered.connect(self.Brown)
        cGray.triggered.connect(self.Gray)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dr = True
            self.lastPoint = event.pos()
            self.point_history += [[self.brColor,  self.brSize, self.lastPoint]]

    def mouseMoveEvent(self, event):

        if self.dr and (event.buttons() == Qt.LeftButton) and self.draw_mode == 'pen':
            painter = QPainter(self.img)
            painter.setPen(QPen(self.brColor, self.brSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.point_history[-1] += [self.lastPoint]
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.dr = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.img, self.img.rect())

    def save(self):
        filePath, _= QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);; ALL Files(*.*)")
        if filePath == "":
            return
        else:
            self.img.save(filePath)

    def clear(self):
        self.img.fill(Qt.white)
        self.update()

    def onePx(self):
        self.brSize = 1

    def twoPx(self):
        self.brSize = 2

    def threePx(self):
        self.brSize = 3

    def fourPx(self):
        self.brSize = 4

    def fivePx(self):
        self.brSize = 5

    def sixPx(self):
        self.brSize = 6

    def sevenPx(self):
        self.brSize = 7

    def eightPx(self):
        self.brSize = 8

    def ninePx(self):
        self.brSize = 9

    def tenPx(self):
        self.brSize = 10

    def Black(self):
        self.brColor = Qt.black

    def Brown(self):
        self.brColor = QColor(153, 51, 0)

    def Gray(self):
        self.brColor = Qt.gray

    def Blue(self):
        self.brColor = Qt.blue

    def Green(self):
        self.brColor = Qt.green

    def Red(self):
        self.brColor = Qt.red

    def LightBlue(self):
        self.brColor = QColor(107, 247, 255)

    def Pink(self):
        self.brColor = QColor(255, 158, 255)

    def Yellow(self):
        self.brColor = Qt.yellow

    def Purple(self):
        self.brColor = QColor(157, 19, 198)

    def back_event(self):
        if self.point_history:
            nowEvent = self.point_history.pop()
            self.events_history += [nowEvent]
            self.brColor = Qt.white
            self.lastPoint = nowEvent[2]
            self.brSize = nowEvent[1]
            painter = QPainter(self.img)
            painter.setPen(QPen(self.brColor, self.brSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            for i in nowEvent[2:]:
                painter.drawLine(self.lastPoint, i)
                self.lastPoint = i
                self.update()

            for i in self.point_history:
                self.brColor = i[0]
                self.brSize = i[1]
                self.lastPoint = i[2]
                painter.setPen(QPen(self.brColor, self.brSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                for j in i[2:]:
                    painter.drawLine(self.lastPoint, j)
                    self.lastPoint = j
                    self.update()

    def forward_event(self):
        if self.events_history:
            event = self.events_history.pop()
            self.point_history += [event]
            self.brColor = event[0]
            self.brSize = event[1]
            self.lastPoint = event[2]
            painter = QPainter(self.img)
            painter.setPen(QPen(self.brColor, self.brSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            for i in event[2:]:
                painter.drawLine(self.lastPoint, i)
                self.lastPoint = i
                self.update()

    def erase(self):
        self.brColor = Qt.white

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
