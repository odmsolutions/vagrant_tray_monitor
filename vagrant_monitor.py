#python2.7
"""Tool to display a tray app - which will monitor the number of running vagrant VM's"""
from __future__ import print_function
import sys
import time

import PySide
from PySide.QtCore import Qt
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QIcon, QSystemTrayIcon, QMessageBox, QPixmap,  QPainter, QPen, QFont

import vagrant_interface

class MonitorWorker(QtCore.QThread):
    updateRunning = QtCore.Signal(int) # Signal when we have another running value

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.vagrant = vagrant_interface.VagrantInterface()
        self.should_stop = False

    def run(self):
        while(not self.should_stop):
            running_count = self.vagrant.get_running_count()
            self.updateRunning.emit(running_count)
            self.msleep(500)


class MonitorUI(object):
    def __init__(self):
        self.close = False
        self.numeric_icons = []
        self.app = None
        self.tray_icon = None
        self.worker = MonitorWorker()
        
    def setup_pixmaps(self):
        # Create pixmaps
        self.original = QPixmap("logo_small.ico")
        numeric_icons = []
        for n in range(0, 9):
            numeric_copy = self.original.copy()
            p = QPainter(numeric_copy)
            p.setPen(QPen(Qt.red))
            p.drawLine(0, 0, 64, 64)
            p.setFont(QFont("sans", 20, QFont.Bold))
            p.drawText(numeric_copy.rect(), Qt.AlignCenter, str(n))
            p.end()
            numeric_icons.append(numeric_copy)
        self.numeric_icons = numeric_icons

    def make_context_menu(self):
        menu = QtGui.QMenu()
        quit_button = menu.addAction("exit")
        QtCore.QObject.connect(quit_button, QtCore.SIGNAL("triggered()"), self.app.exit)
        return menu

    def update_tray(self, running_count):
        self.tray_icon.setToolTip("Running count %d" % running_count)
        self.tray_icon.setIcon(self.numeric_icons[running_count])

    def main(self):
        # Create the application object
        self.app = QApplication(sys.argv)
        
        # Create pixmaps
        self.setup_pixmaps()

        # Create a simple tray app 
        icon = QIcon("logo_small.ico")
        self.tray_icon = QSystemTrayIcon(self.original)
        self.tray_icon.setContextMenu(self.make_context_menu())
        self.tray_icon.setToolTip("Checking vagrant...")

        self.worker.updateRunning.connect(self.update_tray)
        self.worker.start()

        self.tray_icon.show()
        self.app.exec_()
        self.worker.should_stop = True
        self.worker.wait()
        self.tray_icon.hide()
    

def main():
    m = MonitorUI()
    m.main()


main()