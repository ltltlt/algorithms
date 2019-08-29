'''
  > File Name: equeen.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import threading
import time

NUM = 8
con = threading.Condition(threading.RLock())
somelist = None

stepbystep = True

class framework(QtWidgets.QMainWindow):
    # GUI component can only be changed in main thread, that why i use signal and slot.
    # when something happen in child thread, it will signal, and then main thread accept that signal use slot to deal with
    mysignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(max(100*NUM, 600), 30 + max(100*NUM, 600))
        self.center()
        self.setStyleSheet('QWidget { background-color: white ; color: black}')
        self.labelss=[[None]*NUM for i in range(NUM)]
        self.initUI()
        self.statusBar().showMessage('ready')
        self.mysignal.connect(self.showboard)
        self.myaddMenuBar()
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initUI(self):
        self.grid = QtWidgets.QGridLayout()
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.grid)
        self.grid.setSpacing(5)
        for i in range(NUM):
            for j in range(NUM):
                label = QtWidgets.QLabel(self)
                self.grid.addWidget(label, i, j)
                label.setStyleSheet('QLabel { background-color: yellow }')
                self.labelss[i][j] = label
    def resetcolor(self):
        for i in range(NUM):
            for j in range(NUM):
                self.labelss[i][j].setStyleSheet('QLabel { background-color: yellow }')
    def showboard(self, board):
        self.resetcolor()
        for index, i in enumerate(board):
            self.labelss[index][i].setStyleSheet('QLabel { background-image: url(newnew.png) }')
    @staticmethod
    def print_board(arglist):
        for pos in arglist:
            print('_ ' * pos + '@_' + '_ ' * (NUM - pos - 1))
        print()
    @staticmethod
    def check(arglist, i):
        for j in range(len(arglist)):
            if abs(arglist[j] - i) in (0, len(arglist) - j):
                return False
        return True
    @staticmethod
    def checkall(board):
        result = True

        for i in range(len(board)):
            result = result and framework.check(board[:i], board[i])

        return result
    @staticmethod
    def waitfornotify():
        if stepbystep:
            with con:
                con.wait()
        else:
             time.sleep(0.3)
    def set_next_line(self, *already_set_lst):
        next_line = len(already_set_lst)
        if next_line >= NUM:
            self.print_board(already_set_lst)
        else:     
            for i in range(NUM):
                self.mysignal.emit(list(already_set_lst) + [i])
                if self.check(already_set_lst, i):
                    self.statusBar().showMessage('good position')
                    self.waitfornotify()

                    self.set_next_line(*already_set_lst, i)
                else:
                    self.statusBar().showMessage('bad position')
                    self.waitfornotify()
    def runqueens(self):
        nqueens_thread = threading.Thread(target = self.set_next_line, args = ())
        nqueens_thread.setDaemon(True)      # it's ok with linux, but when run in windows, when use ctrl+r, the windows will close
        nqueens_thread.start()
    def hint(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'input dialog', 'give me position: ')
        if ok:
            positions = [int(x)-1 for x in text.split()]
            positions = [x for x in positions if x < NUM]
            self.showboard(positions[0:NUM])
            if self.checkall(positions[0:NUM]):
                self.statusBar().showMessage('no confliction')
            else:
                self.statusBar().showMessage('confliction')
    def myaddMenuBar(self):
        menubar = self.menuBar()
        optionmenu = menubar.addMenu('option')
        self.myaddaction(name = 'hint', shortcutstr = 'ctrl+h', func = self.hint, menu = optionmenu)
        self.myaddaction(name = 'run', shortcutstr = 'ctrl+r', func = self.runqueens, menu = optionmenu)
        self.myaddaction(name = 'quit', shortcutstr = 'ctrl+q', func = self.close, menu = optionmenu)

    def myaddaction(self, name, func, menu, shortcutstr=None):
        action = QtWidgets.QAction(name, self)
        action.setShortcut(shortcutstr)
        action.triggered.connect(func)
        menu.addAction(action)
    def keyPressEvent(self, e):
        global stepbystep
        if e.key() == QtCore.Qt.Key_N:
            with con:
                con.notifyAll()
        elif e.key() == QtCore.Qt.Key_C:
            stepbystep = False
            with con:
                con.notifyAll()
        elif e.key() == QtCore.Qt.Key_S:        # stop
            stepbystep = True                   # not notify
        elif e.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        else:
            e.ignore()


app = QtWidgets.QApplication(sys.argv)

try:
    NUM = int(sys.argv[1])
except (ValueError, IndexError):
    pass
f = framework()
f.statusBar().setFont(QtGui.QFont('DejaVu Sans Mono Bold', 13))
f.show()

sys.exit(app.exec())
