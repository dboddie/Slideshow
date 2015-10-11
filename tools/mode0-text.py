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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication([])
image = QImage(640, 256, QImage.Format_RGB32)

painter = QPainter()
painter.begin(image)

gradient = QLinearGradient(0, 0, 0, 255)
gradient.setColorAt(0, QColor(Qt.white))
gradient.setColorAt(0.25, QColor(Qt.blue))
gradient.setColorAt(0.5, QColor(Qt.red))
gradient.setColorAt(1, QColor(Qt.green))
painter.fillRect(0, 0, 640, 256, gradient)

font = app.font()
font.setPixelSize(64)
painter.setFont(font)
painter.setBrush(QColor(0,0,0))
painter.drawText(QRect(32, 32, 608, 128), Qt.AlignCenter, "MODE 0")
painter.end()

image.save("mode0-text.png")
