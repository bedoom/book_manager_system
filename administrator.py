from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import dbutil
from threading import Thread
from xlsxwriter import *
import time
import datetime
ui, _ = loadUiType('administrator.ui')


class Administrator(QMainWindow, ui):
    def __init__(self, Ano):
        # noinspection PyArgumentList
        super(Administrator, self).__init__()
        self.setupUi(self)
        style = open("themes/darkorange.css", 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.tabWidget_2.tabBar().setVisible(False)
        self.handle_buttons()
        self.Ano = Ano
        self.show_book()
        self.show_user()
        self.show_borrow_book()


    def handle_buttons(self):
        self.pushButton.clicked.connect(self.open_search_tab)
        self.ISBNButton.clicked.connect(self.open_isbn_tab)
        self.borrowButton.clicked.connect(self.open_borrow_tab)
        self.bookButton.clicked.connect(self.open_book_tab)
        self.userButton.clicked.connect(self.open_user_tab)
        self.check_book_button.clicked.connect(self.check_book_tab)
        self.modify_book.clicked.connect(self.modify_book_tab)

        self.name_search_button.clicked.connect(self.name_search)
        self.ISBN_search_button.clicked.connect(self.ISBN_search)

        self.borrow_yes_button.clicked.connect(self.borrow_yes)
        self.borrow_no_button.clicked.connect(self.borrow_no)
        self.record_button.clicked.connect(self.record)
        self.export_day.clicked.connect(self.export_day_operations)

        self.all_book_button.clicked.connect(self.all_book)
        self.onlibrary_button.clicked.connect(self.onlibrary_book)
        self.borrow_book_button.clicked.connect(self.borrow_book)

        self.add_book_button.clicked.connect(self.add_book)
        self.editor_search_button.clicked.connect(self.editor_search)
        self.editor_save_button.clicked.connect(self.editor_save)
        self.delete_search_button.clicked.connect(self.delete_search)
        self.delete_book_button.clicked.connect(self.delete_book)

        self.administrator_save_button.clicked.connect(self.administrator_save)

    def open_search_tab(self):
        self.tabWidget_2.setCurrentIndex(0)

    def open_isbn_tab(self):
        self.tabWidget_2.setCurrentIndex(1)

    def open_borrow_tab(self):
        self.tabWidget_2.setCurrentIndex(2)
        self.show_borrow_book()

    def open_book_tab(self):
        self.tabWidget_2.setCurrentIndex(3)

    def open_user_tab(self):
        self.tabWidget_2.setCurrentIndex(6)

    def check_book_tab(self):
        self.tabWidget_2.setCurrentIndex(4)

    def modify_book_tab(self):
        self.tabWidget_2.setCurrentIndex(5)

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

    def all_book(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select ISBN, Bname, Bauthor, Bpublisher, Bborrow" \
              " from book"

        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
        dbutil.close_conn(conn, cur)
        self.book_search_table.clear()
        if data:
            self.book_search_table.setRowCount(0)
            self.book_search_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.book_search_table.setItem(row, column, QTableWidgetItem(str(item)))
                # column += 1
                row_position = self.book_search_table.rowCount()
                self.book_search_table.insertRow(row_position)
            self.statusBar().showMessage('图书查询成功！')
        else:
            self.statusBar().showMessage('图书馆无藏书！！！请添加图书。')


    def onlibrary_book(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select ISBN, Bname, Bauthor, Bpublisher, Bborrow" \
              " from book where Bborrow='否'"

        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
        dbutil.close_conn(conn, cur)
        self.book_search_table.clear()
        if data:
            self.book_search_table.setRowCount(0)
            self.book_search_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.book_search_table.setItem(row, column, QTableWidgetItem(str(item)))
                # column += 1
                row_position = self.book_search_table.rowCount()
                self.book_search_table.insertRow(row_position)
            self.statusBar().showMessage('图书查询成功！')
        else:
            self.statusBar().showMessage('没有图书在馆')

    def borrow_book(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select ISBN, Bname, Bauthor, Bpublisher, Bborrow" \
              " from book where Bborrow='是'"

        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
        dbutil.close_conn(conn, cur)

        if data:
            # thread = Thread(target=self.borrow_book_func, args=(data,))
            # thread.start()
            self.borrow_book_func(data)
        else:
            self.book_search_table.clear()
            self.statusBar().showMessage('没有图书借阅！！')

    def borrow_book_func(self, data):
        self.book_search_table.clear()
        self.book_search_table.setRowCount(0)
        self.book_search_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.book_search_table.setItem(row, column, QTableWidgetItem(str(item)))
            # column += 1
            row_position = self.book_search_table.rowCount()
            self.book_search_table.insertRow(row_position)
        self.statusBar().showMessage('图书查询成功！')

    def add_book(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "insert into book values (?, ?, ?, ?,?, '否')"
        ISBN = self.add_ISBN_text.text()
        Bname = self.add_book_name.text()
        Bauthor = self.add_author.text()
        Bpublisher = self.add_publisher.text()
        Bdesc = self.add_book_description.toPlainText()
        cur.execute(sql, (ISBN, Bname, Bauthor, Bpublisher, Bdesc))
        conn.commit()
        dbutil.close_conn(conn, cur)
        self.add_ISBN_text.setText('')
        self.add_book_name.setText('')
        self.add_author.setText('')
        self.add_publisher.setText('')
        self.add_book_description.setPlainText('')
        self.show_book()
        self.statusBar().showMessage('书籍添加成功！')

    def editor_search(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select * from book where ISBN=?"
        ISBN = self.editor_search_text.text()
        cur.execute(sql, (ISBN,))
        data = cur.fetchall()
        if data:
            # thread = Thread(target=self.ISBN_search_func, args=(data,))
            # thread.start()
            self.editor_search_func(data)
            self.statusBar().showMessage('图书查询成功！')
        else:
            self.editor_search_text.clear()
            self.editor_book_name.clear()
            self.editor_author.clear()
            self.editor_publisher.clear()
            self.editor_onlibrary.clear()
            self.editor_book_description.clear()
            self.statusBar().showMessage('没有这个书籍！！！')
        dbutil.close_conn(conn, cur)

    def editor_search_func(self, data):
        Bname = data[0][1]
        Bauthor = data[0][2]
        Bpublisher = data[0][3]
        Bdesc = data[0][4]
        Bborrow = data[0][5]
        self.editor_book_name.setText(Bname)
        self.editor_author.setText(Bauthor)
        self.editor_publisher.setText(Bpublisher)
        if Bborrow == '否':
            self.editor_onlibrary.setText('是')
        else:
            self.editor_onlibrary.setText('否')
        self.editor_book_description.setPlainText(Bdesc)

    def editor_save(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "update book set Bname=?, Bauthor=?, Bpublisher=?, Bdesc=? where ISBN=?"

        Bname = self.editor_book_name.text()
        Bauthor = self.editor_author.text()
        Bpublisher = self.editor_publisher.text()
        Bdesc = self.editor_book_description.toPlainText()
        ISBN = self.editor_search_text.text()
        cur.execute(sql, (Bname, Bauthor, Bpublisher, Bdesc, ISBN,))
        conn.commit()
        dbutil.close_conn(conn, cur)
        # print(1)
        self.editor_search_text.setText('')
        self.editor_book_name.setText('')
        self.editor_author.setText('')
        self.editor_publisher.setText('')
        self.editor_book_description.setPlainText('')
        self.editor_onlibrary.setText('')
        self.show_book()
        self.statusBar().showMessage("书籍修改成功！")

    def delete_search(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select * from book where ISBN=?"
        ISBN = self.delete_search_text.text()
        cur.execute(sql, (ISBN,))
        data = cur.fetchall()
        if data:
            # thread = Thread(target=self.ISBN_search_func, args=(data,))
            # thread.start()
            self.delete_search_func(data)
            self.statusBar().showMessage('图书查询成功！')
        else:
            self.delete_search_text.clear()
            self.delete_book_name.clear()
            self.delete_author.clear()
            self.delete_publisher.clear()
            self.delete_onlibrary.clear()
            self.delete_book_description.clear()
            self.statusBar().showMessage('没有这个书籍！！！')
        dbutil.close_conn(conn, cur)

    def delete_search_func(self, data):
        Bname = data[0][1]
        Bauthor = data[0][2]
        Bpublisher = data[0][3]
        Bdesc = data[0][4]
        Bborrow = data[0][5]
        self.delete_book_name.setText(Bname)
        self.delete_author.setText(Bauthor)
        self.delete_publisher.setText(Bpublisher)
        if Bborrow == '否':
            self.delete_onlibrary.setText('是')
        else:
            self.delete_onlibrary.setText('否')
        self.delete_book_description.setPlainText(Bdesc)

    def delete_book(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select Bborrow from book where ISBN=?"
        ISBN = self.delete_search_text.text()
        cur.execute(sql, (ISBN,))
        data = cur.fetchall()
        if not data:
            self.statusBar().showMessage('图书不存在！！！')
        elif data[0][0] == '是':
            self.statusBar().showMessage("书籍出借，不能删除！！！")
        else:
            sql = "delete from book where ISBN=?"
            cur.execute(sql, (ISBN, ))
            conn.commit()
            dbutil.close_conn(conn, cur)
            # print(1)
            self.delete_search_text.setText('')
            self.delete_book_name.setText('')
            self.delete_author.setText('')
            self.delete_publisher.setText('')
            self.delete_book_description.setPlainText('')
            self.delete_onlibrary.setText('')
            self.show_book()
            self.statusBar().showMessage("书籍删除成功！")

    def administrator_save(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "update administrator set Aname=?, Atel=? where Ano=?"
        Aname = self.aname.text()
        Atel = self.atel.text()
        Ano = self.Ano
        cur.execute(sql, (Aname, Atel, Ano,))
        conn.commit()
        dbutil.close_conn(conn, cur)
        self.show_user()
        self.statusBar().showMessage("用户信息修改完毕")
    def borrow_yes(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select Request from borrow where ISBN = ?"
        ISBN = self.borrow_ISBN.text()
        cur.execute(sql, (ISBN, ))
        data = cur.fetchone()
        if data:
            if data[0] == "借阅":
                sql = "update book set Bborrow='是' where ISBN = ?"
                cur.execute(sql, (ISBN, ))
                conn.commit()
                dbutil.close_conn(conn, cur)
                conn = dbutil.get_conn()
                cur = conn.cursor()
                sql = "update borrow set Ano=?, Isagree='是', Timing=? where ISBN=?"
                Timing = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                cur.execute(sql, (self.Ano, Timing, ISBN))
                conn.commit()
            else:
                sql = "update book set Bborrow='否' where ISBN = ?"
                cur.execute(sql, (ISBN,))
                conn.commit()
                dbutil.close_conn(conn, cur)
                conn = dbutil.get_conn()
                cur = conn.cursor()
                sql = "update borrow set Ano=?, Isagree='是', Timing=? where ISBN=?"
                Timing = datetime.date.today()
                cur.execute(sql, (self.Ano, Timing, ISBN))
                conn.commit()

            dbutil.close_conn(conn, cur)
            Thread(self.show_borrow_book()).start()
            self.show_book()
            self.statusBar().showMessage("同意操作成功！")
            self.borrow_ISBN.setText('')

    # def delete_borrow(self, ISBN):
    #     conn = dbutil.get_conn()
    #     cur = conn.cursor()
    #     sql = "delete from borrow where ISBN=?"
    #     cur.execute(sql, (self.Ano,))
    #     conn.commit()

    def borrow_no(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select Request from borrow where ISBN = ?"
        ISBN = self.borrow_ISBN.text()
        cur.execute(sql, (ISBN,))
        data = cur.fetchone()
        if data:
            if data[0] == "借阅":
                sql = "update borrow set Ano=?, Isagree='否', Timing=? where ISBN=?"
                Timing = time.time()
                cur.execute(sql, (self.Ano, Timing, ISBN))
                conn.commit()
            else:
                sql = "update borrow set Ano=?, Isagree='否', Timing=? where ISBN=?"
                Timing = datetime.date.today()
                cur.execute(sql, (self.Ano, Timing, ISBN))
                conn.commit()
            dbutil.close_conn(conn, cur)
            Thread(self.show_borrow_book()).start()
            self.show_book()
            self.statusBar().showMessage("操作成功！")
            self.borrow_ISBN.setText('')


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
        sql = "select Sno, borrow.ISBN, Bname, Request, Day_from, Day_to "\
              "from book, borrow where borrow.ISBN = book.ISBN and borrow.Isagree is null"
        cur.execute(sql)
        data = cur.fetchall()
        if data:
            self.borrow_book_table.setRowCount(0)
            self.borrow_book_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.borrow_book_table.setItem(row, column, QTableWidgetItem(str(item)))
                row_position = self.borrow_book_table.rowCount()
                self.borrow_book_table.insertRow(row_position)

        dbutil.close_conn(conn, cur)

    def show_user(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select * from administrator where Ano=?"
        cur.execute(sql, (self.Ano,))
        data = cur.fetchall()
        self.ano.setText(data[0][0])
        self.aname.setText(data[0][1])
        self.asex.setCurrentText(data[0][2])
        self.atel.setText(data[0][3])
        dbutil.close_conn(conn, cur)

    def export_day_operations(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select Sno, borrow.ISBN, Bname, Day_from, Day_to "\
              "from book, borrow where borrow.Isagree = '是' and borrow.ISBN = book.ISBN"
        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
        wb = Workbook("day_operations.xlsx")
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, "学生学号")
        sheet1.write(0, 1, "ISBN")
        sheet1.write(0, 2, "书名")
        sheet1.write(0, 3, "开始时间")
        sheet1.write(0, 4, "结束时间")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage("数据导出成功！")


    def record(self):
        conn = dbutil.get_conn()
        cur = conn.cursor()
        sql = "select * from borrow where Ano is not null"
        cur.execute(sql)
        data = cur.fetchall()
        self.tabWidget_2.setCurrentIndex(7)
        # print(data)
        if data:
            self.record_table.setRowCount(0)
            self.record_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.record_table.setItem(row, column, QTableWidgetItem(str(item)))
                row_position = self.record_table.rowCount()
                # print(row_position)
                self.record_table.insertRow(row_position)



