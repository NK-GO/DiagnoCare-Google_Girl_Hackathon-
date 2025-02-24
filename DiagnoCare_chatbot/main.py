
import sys
from PyQt5.QtWidgets import QApplication
from gui.mainwindow import MyHealthCareBot
import qdarkstyle

def main():
    app = QApplication(sys.argv)
    bot_window = MyHealthCareBot()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    bot_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
