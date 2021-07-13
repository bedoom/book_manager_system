import datetime

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import dbutil
from threading import Thread

# UI-Logic 分离
ui, _ = loadUiType('student.ui')


class Student(QMainWindow, ui):
    # 定义构造方法
    def __init__(self, Sno):
        super(Student, self).__init__()
        self.setupUi(self)
        style = open("themes/darkorange.css", 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.tabWidget.tabBar().setVisible(False)
        self.handle_buttons()
        self.Sno = Sno
        self.show_book()
        self.show_borrow_book()
        self.show_student()

    # 处理所有button的消息与槽的通信
    def handle_buttons(self):
        self.book_button.clicked.connect(self.open_book_tab)
        self.ISBN_button.clicked.connect(self.open_ISBN_tab)
        self.borrow_button.clicked.connect(self.open_borrow_tab)
        self.user_button.clicked.connect(self.open_user_tab)
        # 01书名查询操作
        self.name_search_button.clicked.connect(self.name_search)
        self.all_books_button.clicked.connect(self.show_book)
        # 02ISBN查询操作
        self.ISBN_search_button.clicked.connect(self.ISBN_search)
        # 03借阅操作
        self.borrow_ISBN_button.clicked.connect(self.borrow_ISBN)
        self.back_ISBN_button.clicked.connect(self.back_ISBN)
        # 04个人操作
        self.student_save_button.clicked.connect(self.student_save)

    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_ISBN_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_borrow_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_user_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def name_search(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select * from book where Bname like ?"
        book_name = self.name_search_text.text()
        cur.execute(sql, (book_name,))
        data = cur.fetchall()
        if data:
            thread = Thread(target=self.name_search_func, args=(data,))
            thread.start()
            self.statusBar().showMessage('图书查询成功！')
        else:
            self.statusBar().showMessage('不存在图书: ' + book_name)
        dbutil.close_conn(conn, cur)

    def name_search_func(self, data):
        # self.name_search_table.clear()
        self.name_search_table.setRowCount(0)
        self.name_search_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.name_search_table.setItem(row, column, QTableWidgetItem(str(item)))
            row_position = self.name_search_table.rowCount()
            self.name_search_table.setRowCount(row_position)

    def ISBN_search(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select * from book where ISBN=?"
        ISBN = self.ISBN_search_text.text()
        cur.execute(sql, (ISBN,))
        data = cur.fetchall()
        if data:
            # thread = Thread(target=self.ISBN_search_func, args=(data,))
            # thread.start()
            self.ISBN_search_func(data)
            self.statusBar().showMessage('图书查询成功！')
        else:
            self.ISBN_search_text.clear()
            self.ISBN_book_name.clear()
            self.ISBN_author.clear()
            self.ISBN_publisher.clear()
            self.ISBN_onlibrary.clear()
            self.ISBN_decription.clear()
            self.statusBar().showMessage('没有这个书籍！！！')
        dbutil.close_conn(conn, cur)

    def ISBN_search_func(self, data):
        Bname = data[0][1]
        Bauthor = data[0][2]
        Bpublisher = data[0][3]
        Bdesc = data[0][4]
        Bborrow = data[0][5]
        self.ISBN_book_name.setText(Bname)
        self.ISBN_author.setText(Bauthor)
        self.ISBN_publisher.setText(Bpublisher)
        if Bborrow == '否':
            self.ISBN_onlibrary.setText('是')
        else:
            self.ISBN_onlibrary.setText('否')
        self.ISBN_decription.setPlainText(Bdesc)

    def borrow_ISBN(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select Bborrow from book where ISBN=?"
        ISBN = self.borrow_ISBN_text.text()
        cur.execute(sql, (ISBN,))
        data = cur.fetchall()
        # print(data)
        if data:
            if data[0][0] == "否":
                sql = "select * from borrow where ISBN=?"
                cur.execute(sql, (ISBN, ))
                data = cur.fetchone()
                if data:
                    if data[3]:
                        sql = "delete from borrow where ISBN = ?"
                        cur.execute(sql, (ISBN, ))
                        conn.commit()
                        sql = "insert into borrow(Ano, ISBN, Sno, Request, Isagree, Day_from, Day_to, Timing) values (null, ?, ?, ?, null, ?, ?, null)"
                        day_number = self.day_combox.currentIndex() + 1
                        today_date = datetime.date.today()
                        to_day = today_date + datetime.timedelta(days=day_number)
                        cur.execute(sql, (ISBN, self.Sno, '借阅', today_date, to_day))
                        conn.commit()
                        self.statusBar().showMessage('等待管理员同意ing')
                    else:
                        self.statusBar().showMessage("已经有人借阅，正等待管理员同意")
                else:
                    sql = "insert into borrow(Ano, ISBN, Sno, Request, Isagree, Day_from, Day_to, Timing) values (null, ?, ?, ?, null, ?, ?, null)"
                    day_number = self.day_combox.currentIndex() + 1
                    today_date = datetime.date.today()
                    to_day = today_date + datetime.timedelta(days=day_number)
                    cur.execute(sql, (ISBN, self.Sno, '借阅', today_date, to_day))
                    conn.commit()
                    self.statusBar().showMessage('等待管理员同意ing')
            else:
                self.statusBar().showMessage("此书已出借")
        else:
            self.statusBar().showMessage('没有这本书！！！')
        dbutil.close_conn(conn, cur)

    def back_ISBN(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = """select *
                from borrow
                where ISBN = ? and Sno=? and Isagree='是'"""
        ISBN = self.borrow_ISBN_text.text()
        cur.execute(sql, (ISBN, self.Sno))
        data = cur.fetchall()
        # print(data)
        if data:
            sql = """update borrow set Ano=null, Isagree=null, Request='归还', Timing=null where ISBN = ? and Sno = ?"""
            cur.execute(sql, (ISBN, self.Sno))
            conn.commit()
            self.statusBar().showMessage('等待管理员同意ing')
        else:
            self.statusBar().showMessage('没有这本书！！！')
        dbutil.close_conn(conn, cur)
        self.show_borrow_book()

    def student_save(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "update student set Stel = ? where Sno = ?"
        tel = self.student_stel.text()
        cur.execute(sql, (tel, self.Sno))
        conn.commit()
        dbutil.close_conn(conn, cur)
        self.statusBar().showMessage('用户信息更改成功')
        self.show_student()


    def show_student(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select *" \
              " from student"

        cur.execute(sql)
        data = cur.fetchall()
        # print(data)

        self.student_sno.setText(data[0][0])
        self.student_sname.setText(data[0][1])
        self.student_ssex.setCurrentText(data[0][2])
        self.student_stel.setText(data[0][3])
        self.student_sdept.setCurrentText(data[0][4])

        dbutil.close_conn(conn, cur)


    def show_book(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select ISBN, Bname, Bauthor, Bpublisher, Bborrow" \
              " from book"

        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
        dbutil.close_conn(conn, cur)
        if data:
            self.name_search_table.setRowCount(0)
            self.name_search_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.name_search_table.setItem(row, column, QTableWidgetItem(str(item)))
                # column += 1
                row_position = self.name_search_table.rowCount()
                self.name_search_table.insertRow(row_position)

    def show_borrow_book(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = """
                select book.ISBN, Bname, Bauthor, Bpublisher, Day_from, Day_to
                from borrow, book
                where borrow.ISBN = book.ISBN and Sno=? and (borrow.Isagree='是' and borrow.Request='借阅' or borrow.Isagree='否' and borrow.Request='归还')
            """
        cur.execute(sql, (self.Sno,))
        data = cur.fetchall()
        if data:
            self.borrow_book_table.setRowCount(0)
            self.borrow_book_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.borrow_book_table.setItem(row, column, QTableWidgetItem(str(item)))
                row_position = self.borrow_book_table.rowCount()
                self.borrow_book_table.insertRow(row_position)
