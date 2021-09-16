import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PWS_Main import *
import StartUp
import Register
import Menu
import validator as vd
import sqlite3

class StartUp(QMainWindow, StartUp.Ui_MainWindow):
    def __init__(self, parent = None):
        from os import mkdir
        super(StartUp, self).__init__(parent)
        try:
            mkdir('data')
        except FileExistsError:
            pass
        self.conn = sqlite3.connect('data/registry.db')
        self.curs = self.conn.cursor()
        try:
            self.curs.execute('''CREATE TABLE registry(username TEXT PRIMARY KEY, pw TEXT NOT NULL)''')
        except sqlite3.OperationalError:
            pass
        self.setupUi(self)
        self.window2 = None
        #-----register buttons below this line------
        self.pb_register.clicked.connect(self._register)
        self.pb_login.clicked.connect(self._login)
    # ---------define button functions below this line ---------
    def _register(self):
        self.window2 = Register()
        self.conn.commit()
        self.conn.close()
        self.close()
        self.window2.show()

    def _login(self):
        global current_user
        current_user = self.le_account.text().casefold()
        pw = self.le_password.text()

        # if uid not found in db --> "no user found"
        user_list = [i for i in self.curs.execute('''SELECT username FROM registry''').fetchall()[0]]
        if current_user not in user_list:
            self.le_account.setText('User not found.')
        # if uid found but bad pw --> "incorrect password"
        else:
            users_pw = self.curs.execute('''SELECT pw FROM registry WHERE username = (?)''', tuple([current_user])).fetchone()[0]
            if pw != users_pw:
                self.le_password.setText('Incorrect password.')
            else:
                self.window2 = Menu()
                self.conn.commit()
                self.conn.close()
                self.close()
                self.window2.show()
            
class Register(QMainWindow, Register.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Register, self).__init__(parent)
        self.conn = sqlite3.connect('data/registry.db')
        self.curs = self.conn.cursor()
        self.setupUi(self)
        self.window2 = None
        #-----register buttons below this line---------
        self.pb_cancel.clicked.connect(self._cancel)
        self.pb_ok.clicked.connect(self._ok)
    #--------define functions---------
    def _cancel(self):
        self.window2 = StartUp()
        self.close()
        self.window2.show()

    def _ok(self):
        uid = self.le_user.text().casefold()
        pw = self.le_pw.text()
        try:
            if uid != '':
                self.err_msg_user.setText('')
                if len(pw) < 4:
                    self.err_msg_pw.setText('<html><head/><body><p><span style=" color:#ff0000;">Invalid password.</span></p></body></html>')
                else:
                    _COMB = [(uid, pw)]
                    self.curs.executemany('INSERT INTO registry VALUES (?, ?)', _COMB)
                    self.conn.commit()
                    self.conn.close()
                    self.window2 = StartUp()
                    self.close()
                    self.window2.show()
        except sqlite3.IntegrityError:
            self.err_msg_user.setText('<html><head/><body><p><span style=" color:#ff0000;">Username already taken.</span></p></body></html>')        
            self.err_msg_pw.setText('')

class Menu(QWidget, Menu.Ui_Form):
    def __init__(self, parent = None):
        super(Menu, self).__init__(parent)
        self.setupUi(self)
        self.window2 = None
        #-------register buttons--------
        self.pb_gen.clicked.connect(self._gen)
        self.pb_lu.clicked.connect(self._lookup)
    #------define functions---------
    def _gen(self):
        self.window2 = Core()
        self.close()
        self.window2.show()

    def _lookup(self):
        # to be coded
        pass

class Core(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(Core, self).__init__(parent)
        self.conn = sqlite3.connect('data/sqlPWS.db')
        self.cursor = self.conn.cursor()
        
        try:
            # research for creating different tables using dynamic table name based on login user
            self.cursor.execute('''CREATE TABLE pws(cheque TEXT PRIMARY KEY, app TEXT NOT NULL, uid TEXT NOT NULL, pw TEXT NOT NULL, user TEXT NOT NULL)''')
        except sqlite3.OperationalError:
            pass
        self.setupUi(self)
        self.window2 = None
        # -----register the buttons below this line---------
        self.pb_quit.clicked.connect(self._close) # quit the application when clicked
        self.pb_run.clicked.connect(self._run)    # click to start password generation
        self.pb_save.clicked.connect(self._save)  # click to save the current app name, uid and password
        self.pb_copy.clicked.connect(self._copy)
        self.pb_main_menu.clicked.connect(self._return)
    #--------define buttons functions below this line---------
    # to disconnect from the database and to close the application
    def _close(self):
        self.conn.close()
        self.close()

    # to generate password combination
    def _run(self): 
        # dfet = digit for each type
        dfet = {}
        
        num = self.num_y.isChecked()
        upl = self.upl_y.isChecked()
        lwl = self.lwl_y.isChecked()
        sym = self.sym_y.isChecked()
        pw_len = self.digits_need.value()
           
        try:
            self.err_comb_label1.setText('')
            self.err_comb_label2.setText('')

            if num == True:
                dfet['num'] = 1

            if upl == True:
                dfet['upl'] = 1

            if lwl == True:
                dfet['lwl'] = 1

            if sym == True:
                dfet['sym'] = 1

            curr_len = sum(dfet.values())
            need_char_len = pw_len - curr_len

            vd.determinator(dfet, need_char_len)
            password = vd.generator(dfet)

            self.pws_pw.setText(password)

        except ValueError:
            # to check if the types of characters required exceed the length requested
            self.err_comb_label1.setText('<html><head/><body><p><span style=" color:#ff0000;">Impossible combination.</span></p></body></html>')
            self.err_comb_label2.setText('<html><head/><body><p><span style=" color:#ff0000;">Please check your input.</span></p></body></html>')

    # to save the app name, user id, and generated password to database for further access
    def _save(self):

        _comb = [(self.appname_line.text().title() + self.user_id.text().upper(),
                  self.appname_line.text().title(),
                  self.user_id.text().upper(),
                  self.pws_pw.text(),
                  current_user
                  )]

        if self.appname_line.text() == "":
            self.err_msg_appname.setText('<html><head/><body><p><span style=" color:#ff0000;">Please enter application/website name.</span></p></body></html>')
        elif self.user_id.text() == "":
            self.err_msg_appname.setText('')
            self.err_msg_uid.setText('<html><head/><body><p><span style=" color:#ff0000;">Please enter user ID.</span></p></body></html>')
        elif self.pws_pw.text() == "":
            self.err_msg_uid.setText('')
            self.err_msg_pw.setText('<html><head/><body><p><span style=" color:#ff0000;">Please click Run to generate a password.</span></p></body></html>')
        else:        
            self.err_msg_pw.setText('')
            try:
                self.cursor.executemany('''INSERT INTO pws VALUES (?, ?, ?, ?, ?)''', _comb)
                self.conn.commit()

            # if app name already exists
            except sqlite3.IntegrityError:
                # code to be filled in
                # ask if overwrite
                print('duplicate primary key')
                pass

    def _copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.pws_pw.text())

    def _return(self):
        self.window2 = Menu()
        self.conn.close()
        self.close()
        self.window2.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    startup = StartUp()

    startup.show()
    sys.exit(app.exec())
