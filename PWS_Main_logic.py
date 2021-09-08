import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PWS_Main import *
import validator as vd

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MyMainWindow, self).__init__(parent)

        self.setupUi(self)
        # -----register the buttons below this line---------
        self.pb_quit.clicked.connect(self.close) # quit the application when clicked
        self.pb_run.clicked.connect(self.run)    # click to start password generation

    #--------define buttons functions below this line---------
    def run(self):

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_Win = MyMainWindow()
    my_Win.show()
    app.exec() # in PyQt6 the underscore suffix is omitted app.exec_() is no longer valid

