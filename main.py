import sys

from root import Root
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main = Root()
    main.show()
    sys.exit(app.exec_())