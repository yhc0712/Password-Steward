import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QMessageBox, QWidget
from PWS_Main import *
import StartUp
import Register
import Menu
import lookup
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
        self.le_password.selectionChanged.connect(self._echo)
    # ---------define button functions below this line ---------
    def _register(self):
        self.window2 = Register()
        self.conn.commit()
        self.conn.close()
        self.close()
        self.window2.show()

    def _echo(self):
        self.le_password.clear()
        self.le_password.setEchoMode(QLineEdit.EchoMode.Password)

    def _login(self):
        global current_user
        current_user = self.le_account.text().casefold()
        pw = self.le_password.text()

        # if uid not found in db --> "no user found"
        user_list = []
        for i in self.curs.execute('''SELECT username FROM registry''').fetchall():
            user_list.append(i[0])
        if current_user not in user_list:
            self.le_account.setText('User not found.')
        # if uid found but bad pw --> "incorrect password"
        else:
            users_pw = self.curs.execute('''SELECT pw FROM registry WHERE username = (?)''', tuple([current_user])).fetchone()[0]
            if pw != users_pw:
                self.le_password.setEchoMode(QLineEdit.EchoMode.Normal)
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
        self.conn.close()
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
        self.window2 = Lookup()
        self.close()
        self.window2.show()        

class Lookup(QWidget, lookup.Ui_Dialog):
    def __init__(self, parent=None):
        super(Lookup, self).__init__(parent)
        self.setupUi(self)
        self.window2 = None
        self.conn = sqlite3.connect('data/sqlPWS.db')
        self.cursor = self.conn.cursor()
        _app_current_user = ['']
        _user = [current_user]
        _apps = self.cursor.execute('SELECT DISTINCT app FROM pws WHERE user = (?);', _user).fetchall()
        for i in _apps:
            _app_current_user.append(i[0])
        # buttons
        self.pb_update.clicked.connect(self._update)
        self.pb_cp.clicked.connect(self._copy)
        self.pb_ok.clicked.connect(self._ok)
        self.pb_check.clicked.connect(self._check)
        #combo box contents
        self.cb_app.addItems(_app_current_user)
        self.cb_app.activated.connect(self._sel_uid)
        self.cb_uid.currentIndexChanged.connect(self._clear_pw)
    # functions
    def _check(self):
        _cheque = [self.cb_app.currentText() + self.cb_uid.currentText() + current_user]
        _pw = self.cursor.execute('SELECT pw FROM pws WHERE cheque = (?);', _cheque).fetchone()
        try:
            self.lu_pw.setText(_pw[0])
        except TypeError:
            pass

    def _sel_uid(self):
        self.cb_uid.clear()
        self.lu_pw.clear()
        _current_app = self.cb_app.currentText()
        _user_uid = [current_user, _current_app]
        _current_app_uid = []
        _uids = self.cursor.execute('SELECT uid FROM pws WHERE user = (?) AND app = (?);', _user_uid).fetchall()
        for j in _uids:
            _current_app_uid.append(j[0])
        self.cb_uid.addItems(_current_app_uid)

    def _clear_pw(self):
        self.lu_pw.clear()

    def _update(self):
        self.window2 = Core()
        self.close()
        self.window2.show()

    def _copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.lu_pw.text())

    def _ok(self):
        self.window2 = Menu()
        self.close()
        self.window2.show()

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

        # the first element is concatenation of app name, user id of the app, and the current user as a primary key to prevent duplicate account of the same app for the current user
        _comb = [(self.appname_line.text().title() + self.user_id.text().upper() + current_user,
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
                self._msg()
                # ask if overwrite
                

    def _copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.pws_pw.text())

    def _return(self):
        self.window2 = Menu()
        self.conn.close()
        self.close()
        self.window2.show()

    def _msg(self):
        from math import log2
        # message box pops up if duplicate app name for the same user
        reply = QMessageBox.question(self, "Existing App", "The username you intended to generate a password for the designated app already exists. Do you want to overwrite its password?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No )
        # the return values of QMessageBox of standard buttons yes and no are exponents to the base 2, where yes has exponents of 14 and no 16
        a = int(log2(int(reply)))
        if a == 14: # if the reply is "YES"
            # overwrite the password
            _new_pw = self.pws_pw.text()
            _new_comb = [_new_pw, current_user, self.appname_line.text().title(), self.user_id.text().upper()]
            self.cursor.execute('''UPDATE pws
                                    SET pw = (?)
                                    WHERE user = (?)
                                    AND app = (?)
                                    AND uid = (?);''', _new_comb)
            self.conn.commit()
        else:
            # do nothing, close the message box
            reply = QMessageBox.about(self, "Information", "Your password has not been udpated.")
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    startup = StartUp()
    startup.show()
    sys.exit(app.exec())
