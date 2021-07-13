import hashlib

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import dbutil
from administrator import Administrator
from threading import Thread
from student import Student

ui, _ = loadUiType('log.ui')


class LoginAPP(QWidget, ui):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.loginbutton.clicked.connect(self.handel_login)
        style = open("themes/darkorange.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    # MD5处理
    def md5(self, arg):
        hash = hashlib.md5()
        hash.update(bytes(arg, encoding='utf-8'))
        return hash.hexdigest()

    def handel_login(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select * from users where username=? and pwd=?"
        user_name = self.username.text()
        pwd = self.pwd.text()
        # pwd = self.md5(pwd)
        cur.execute(sql, (user_name, pwd))
        data = cur.fetchone()
        # print(data)
        if data:
            sql = "select * from student where Sno=?"
            cur.execute(sql, (data[0],))
            flag = cur.fetchone()
            if flag:
                self.mainApp = Student(data[0])
            else:
                self.mainApp = Administrator(data[0])
            self.close()
            self.mainApp.show()


        else:
            self.error_message.setText("用户名或密码错误，重新输入")
