from PyQt5.QtWidgets import *
from log import LoginAPP
import sys


app = QApplication([])
window = LoginAPP()
# window = Student('20191102048')
# login_dialog = Ui_LoginDialog()
# login_dialog.setupUi(window)
window.show()
sys.exit(app.exec_())



