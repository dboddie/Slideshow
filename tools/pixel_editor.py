#!/usr/bin/env python

"""
Copyright (C) 2015 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

pixel_icon = (
    ".....",
    ".....",
    "..x..",
    ".....",
    "....."
    )

flood_icon = (
    ".....",
    ".....",
    "xxxxx",
    ".....",
    "....."
    )

class PictureWidget(QWidget):

    def __init__(self, width = 640, height = 256,
                       xscale = 1, yscale = 2, parent = None):
    
        QWidget.__init__(self, parent)
        
        self.image = QImage(width, height, QImage.Format_RGB32)
        self.clearPicture()
        
        self.xs = xscale
        self.ys = yscale
        self.scale = 1
        self.colour = QColor(Qt.white)
        self.tool = "pixel"
        
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        
        self.setMouseTracking(True)
    
    def clearPicture(self):
    
        self.image.fill(qRgb(0, 0, 0))
    
    def loadPicture(self, path):
    
        return self.image.load(path)
    
    def savePicture(self, path):
    
        return self.image.save(path)
    
    def setCurrentColour(self, colour):
    
        self.colour = colour
    
    def setTool(self, tool):
    
        self.tool = tool
    
    def changeZoom(self, change):
    
        self.scale = max(1, min(self.scale + change, 16))
        self.adjustSize()
    
    def mousePressEvent(self, event):
    
        r = self._row_from_y(event.y())
        c = self._column_from_x(event.x())
        
        if self.tool == "pixel":
            if event.button() == Qt.LeftButton:
                self.writePixel(c, r, self.colour.rgb())
            elif event.button() == Qt.MiddleButton:
                self.writePixel(c, r, qRgb(0, 0, 0))
            else:
                event.ignore()
        
        elif self.tool == "flood":
            if event.button() == Qt.LeftButton:
                self.writeLine(c, r, self.colour.rgb())
            elif event.button() == Qt.MiddleButton:
                self.writeLine(c, r, qRgb(0, 0, 0))
            else:
                event.ignore()
        else:
            event.ignore()
    
    def mouseMoveEvent(self, event):
    
        r = self._row_from_y(event.y())
        c = self._column_from_x(event.x())
        
        if self.tool == "pixel":
            if event.buttons() & Qt.LeftButton:
                self.writePixel(c, r, self.colour.rgb())
            elif event.buttons() & Qt.MiddleButton:
                self.writePixel(c, r, qRgb(0, 0, 0))
            else:
                event.ignore()
        
        elif self.tool == "flood":
            if event.buttons() & Qt.LeftButton:
                self.writeLine(c, r, self.colour.rgb())
            elif event.buttons() & Qt.MiddleButton:
                self.writeLine(c, r, qRgb(0, 0, 0))
            else:
                event.ignore()
        else:
            event.ignore()
    
    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.scale(self.scale * self.xs, self.scale * self.ys)
        painter.drawImage(0, 0, self.image)
        painter.end()
    
    def sizeHint(self):
    
        return QSize(self.image.width() * self.scale * self.xs,
                     self.image.height() * self.scale * self.ys)
    
    def _row_from_y(self, y):
    
        return y/(self.scale * self.ys)
    
    def _column_from_x(self, x):
    
        return x/(self.scale * self.xs)
    
    def _y_from_row(self, r):
    
        return r * self.scale * self.ys
    
    def _x_from_column(self, c):
    
        return c * self.scale * self.xs
    
    def writePixel(self, c, r, value):
    
        if c < 0 or c >= self.image.width() or r < 0 or r >= self.image.height():
            return
        
        self.image.setPixel(c, r, value)
        self.update(QRect(self._x_from_column(c), self._y_from_row(r),
              self.scale * self.xs, self.scale * self.ys))
    
    def writeLine(self, c, r, value):
    
        if c < 0 or c >= self.image.width() or r < 0 or r >= self.image.height():
            return
        
        x = 0
        while x < self.image.width():
            self.image.setPixel(x, r, value)
            x += 1
        
        self.update(QRect(self._x_from_column(0), self._y_from_row(r),
              self.image.width() * self.scale * self.xs, self.scale * self.ys))


class EditorWindow(QMainWindow):

    def __init__(self):
    
        QMainWindow.__init__(self)
        
        self.path = ""
        
        self.pictureWidget = PictureWidget()
        
        self.createToolBars()
        self.createMenus()
        
        self.colourGroup.actions()[0].trigger()
        self.toolGroup.actions()[0].trigger()
        
        self.area = QScrollArea()
        self.area.setWidget(self.pictureWidget)
        self.setCentralWidget(self.area)
        self.setWindowTitle(self.tr("Pixel Editor"))
    
    def newFile(self):
    
        sizeDialog = QDialog()
        
        widthEdit = QSpinBox()
        widthEdit.setRange(1, 640)
        widthEdit.setValue(640)
        heightEdit = QSpinBox()
        heightEdit.setRange(1, 256)
        heightEdit.setValue(256)
        
        aspectCombo = QComboBox()
        aspectCombo.addItem(self.tr("1:1"))
        aspectCombo.addItem(self.tr("1:2"))
        aspectCombo.addItem(self.tr("2:1"))
        
        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.Ok).clicked.connect(sizeDialog.accept)
        buttons.addButton(QDialogButtonBox.Cancel).clicked.connect(sizeDialog.reject)
        
        layout = QFormLayout(sizeDialog)
        layout.addRow(self.tr("&Width:"), widthEdit)
        layout.addRow(self.tr("&Height:"), heightEdit)
        layout.addRow(self.tr("&Aspect ratio:"), aspectCombo)
        layout.addRow(buttons)
        
        if sizeDialog.exec_() == QDialog.Accepted:
        
            # Remove the existing picture widget and discard it.
            self.area.takeWidget()
            
            xscale, yscale = [(1, 1), (1, 2), (2, 1)][aspectCombo.currentIndex()]
            self.pictureWidget = PictureWidget(width = widthEdit.value(),
                                               height = heightEdit.value(),
                                               xscale = xscale, yscale = yscale)
            self.area.setWidget(self.pictureWidget)
    
    def openFile(self):
    
        path = QFileDialog.getOpenFileName(self, self.tr("Open File"),
                                           self.path, self.tr("PNG file (*.png)"))
        if not path.isEmpty():
        
            if self.pictureWidget.loadPicture(unicode(path)):
                self.path = path
                self.setWindowTitle(self.tr("%1 - Pixel Editor").arg(path))
            else:
                QMessageBox.warning(self, self.tr("Open File"),
                    self.tr("Couldn't open the image '%1'.\n").arg(path))
        
    def saveAs(self):
    
        path = QFileDialog.getSaveFileName(self, self.tr("Save Picture"),
                                           self.path, self.tr("PNG file (*.png)"))
        if not path.isEmpty():
        
            if self.pictureWidget.savePicture(unicode(path)):
                self.path = path
                self.setWindowTitle(self.tr("%1 - Pixel Editor").arg(path))
            else:
                QMessageBox.warning(self, self.tr("Save Picture"),
                    self.tr("Couldn't save the image to '%1'.\n").arg(path))
    
    def createToolBars(self):
    
        self.colourGroup = QActionGroup(self)
        
        toolBar = QToolBar(self.tr("Colours"))
        self.addToolBar(Qt.TopToolBarArea, toolBar)
        
        for i in range(8):
        
            image = QImage(16, 16, QImage.Format_RGB32)
            r = (i & 1) * 255
            g = ((i >> 1) & 1) * 255
            b = ((i >> 2) & 1) * 255
            s = "#%02x%02x%02x" % (r, g, b)
            image.fill(qRgb(r, g, b))
            
            icon = QIcon(QPixmap.fromImage(image))
            action = toolBar.addAction(icon, str(i))
            action.setData(QVariant(s))
            action.setCheckable(True)
            self.colourGroup.addAction(action)
            action.triggered.connect(self.setCurrentColour)
        
        self.toolGroup = QActionGroup(self)
        
        toolBar = QToolBar(self.tr("Colours"))
        self.addToolBar(Qt.TopToolBarArea, toolBar)
        
        tools = [(self.tr("Pixel"), pixel_icon, "pixel"),
                 (self.tr("Flood"), flood_icon, "flood")]
        
        colours = {'.': qRgb(0, 0, 0), 'x': qRgb(255, 0, 0)}
        
        for name, image_data, tool in tools:
        
            image = QImage(5, 5, QImage.Format_RGB32)
            image.fill(qRgb(0, 0, 0))
            for y in range(5):
                for x in range(5):
                    image.setPixel(x, y, colours[image_data[y][x]])
            
            icon = QIcon(QPixmap.fromImage(image.scaled(16, 16)))
            
            action = toolBar.addAction(icon, name)
            action.setData(QVariant(tool))
            action.setCheckable(True)
            self.toolGroup.addAction(action)
            action.triggered.connect(self.setTool)
    
    def createMenus(self):
    
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        
        newAction = fileMenu.addAction(self.tr("&New"))
        newAction.setShortcut(QKeySequence.New)
        newAction.triggered.connect(self.newFile)
        
        openAction = fileMenu.addAction(self.tr("&Open..."))
        openAction.setShortcut(QKeySequence.Open)
        openAction.triggered.connect(self.openFile)
        
        saveAsAction = fileMenu.addAction(self.tr("Save &As..."))
        saveAsAction.setShortcut(QKeySequence.SaveAs)
        saveAsAction.triggered.connect(self.saveAs)
        
        quitAction = fileMenu.addAction(self.tr("E&xit"))
        quitAction.setShortcut(self.tr("Ctrl+Q"))
        quitAction.triggered.connect(self.close)
        
        editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        clearAction = editMenu.addAction(self.tr("&Clear"))
        clearAction.triggered.connect(self.clearPicture)
        
        viewMenu = self.menuBar().addMenu(self.tr("&View"))
        zoomInAction = viewMenu.addAction(self.tr("Zoom &In"))
        zoomInAction.setShortcut(self.tr("Ctrl++"))
        zoomInAction.triggered.connect(self.zoomIn)
        zoomOutAction = viewMenu.addAction(self.tr("Zoom &Out"))
        zoomOutAction.setShortcut(self.tr("Ctrl+-"))
        zoomOutAction.triggered.connect(self.zoomOut)
    
    def clearPicture(self):
    
        answer = QMessageBox.question(self, self.tr("Clear Picture"),
            self.tr("Clear the current picture?"), QMessageBox.Yes | QMessageBox.No)
        
        if answer == QMessageBox.Yes:
            self.pictureWidget.clearPicture()
    
    def setCurrentColour(self):
    
        self.pictureWidget.setCurrentColour(QColor(self.sender().data().toString()))
    
    def setTool(self):
    
        self.pictureWidget.setTool(unicode(self.sender().data().toString()))
    
    def zoomIn(self):
    
        self.pictureWidget.changeZoom(1)
    
    def zoomOut(self):
    
        self.pictureWidget.changeZoom(-1)
    
    def sizeHint(self):
    
        pictureSize = self.pictureWidget.sizeHint()
        menuSize = self.menuBar().sizeHint()
        scrollBarSize = self.centralWidget().verticalScrollBar().size()
        
        return QSize(max(pictureSize.width(), menuSize.width(), pictureSize.width()),
                     pictureSize.height() + menuSize.height() + scrollBarSize.height())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    window = EditorWindow()
    window.show()
    
    sys.exit(app.exec_())
