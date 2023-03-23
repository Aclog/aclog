import sys,os
import mysql.connector as con
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem,QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtCore,  QtWidgets
from passlib.hash import pbkdf2_sha256
from re import fullmatch
from configparser import ConfigParser
from os.path import isfile
import aclog,insert_db
from functools import partial
from datetime import datetime


class LoginApp(QDialog):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi("login-form.ui", self)
        if isfile('MyApp_config.ini'):
            pass
        else:
            config = ConfigParser()
            config["mysql_database"] = {
                "host": "",
                "user": "",
                "password": "",
                "db": ""
            }
            with open('MyApp_config.ini', 'w') as conf:
                config.write(conf)
            QMessageBox.information(self, "MyApp", "Fill in the config file!")
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)

    def login(self):
        un = self.tb1.text()
        pw = self.tb2.text()

        if len(un) < 2:
            QMessageBox.information(self, "MyApp", "The minimum Username length is 2 characters!")
        elif len(un) > 30:
            QMessageBox.information(self, "MyApp", "The maximum Username length is 30 characters!")
        elif len(pw) < 6:
            QMessageBox.information(self, "MyApp", "The minimum Password length is 6 characters!")
        elif len(pw) > 100:
            QMessageBox.information(self, "MyApp", "The maximum Password length is 100 characters!")
        else:
            config = ConfigParser()
            config.read("MyApp_config.ini")
            database = config["mysql_database"]
            db_host = database["host"]
            db_user = database["user"]
            db_password = database["password"]
            db_db = database["db"]
            try:
                db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
                cur = db.cursor()
                cur.execute("select password from users where username='" + un + "'")
                result_pw = cur.fetchone()
                try:
                    if pbkdf2_sha256.verify(pw, str(result_pw[0])):
                        QMessageBox.information(self, "MyApp", "You have successfully logged in!")
                        self.tb1.setText("")
                        self.tb2.setText("")


                        w.setCurrentIndex(3)

                except:
                    QMessageBox.information(self, "MyApp", "Couldn't find an account")
            except:
                QMessageBox.information(self, "MyApp",
                                        "There is no connection to the database, fill in the config file!")

    def show_reg(self):
        w.setCurrentIndex(1)

class RegApp(QDialog):
    def __init__(self):
        super(RegApp, self).__init__()
        loadUi("register-form.ui", self)
        if isfile('MyApp_config.ini'):
            pass
        else:
            config = ConfigParser()
            config["mysql_database"] = {
                "host": "",
                "user": "",
                "password": "",
                "db": ""
            }
            with open('MyApp_config.ini', 'w') as conf:
                config.write(conf)
            QMessageBox.information(self, "MyApp", "Fill in the config file!")
        self.b3.clicked.connect(self.reg)
        self.b4.clicked.connect(self.show_login)

    def reg(self):
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()

        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if len(un) < 2:
            QMessageBox.information(self, "MyApp", "The minimum Username length is 2 characters!")
        elif len(un) > 30:
            QMessageBox.information(self, "MyApp", "The maximum Username length is 30 characters!")
        elif len(pw) < 6:
            QMessageBox.information(self, "MyApp", "The minimum Password length is 6 characters!")
        elif len(pw) > 100:
            QMessageBox.information(self, "MyApp", "The maximum Password length is 100 characters!")
        elif not fullmatch(regex, em):
            QMessageBox.information(self, "MyApp", "Invalid Email!")
        elif len(em.split("@")[0]) < 5:
            QMessageBox.information(self, "MyApp", "The minimum Email length is 5 characters!")
        elif len(em.split("@")[0]) > 100:
            QMessageBox.information(self, "MyApp", "The maximum Email length is 100 characters!")
        else:
            config = ConfigParser()
            config.read("MyApp_config.ini")
            database = config["mysql_database"]
            db_host = database["host"]
            db_user = database["user"]
            db_password = database["password"]
            db_db = database["db"]
            try:
                db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
                cur = db.cursor()
                cur.execute("select username from users where username='" + un + "'")
                result_un = cur.fetchone()
                if result_un:
                    QMessageBox.information(self, "MyApp", "The user is already registered")
                else:
                    cur.execute("insert into users values('" + un + "', '" +
                                pbkdf2_sha256.hash(pw) + "', '" + em + "')")
                    db.commit()
                    QMessageBox.information(self, "MyApp", "The user has been successfully registered!")
                    self.tb3.setText("")
                    self.tb4.setText("")
                    self.tb5.setText("")
                    w.setCurrentIndex(0)
            except:
                QMessageBox.information(self, "MyApp",
                                        "There is no connection to the database, fill in the config file!")

    def show_login(self):
        w.setCurrentIndex(0)

class show_database_log(QDialog):
    def __init__(self):
        super(show_database_log, self).__init__()
        loadUi("query_database.ui", self)
        self.b5.clicked.connect(self.select_data)
        self.pushButton.clicked.connect(self.return_button)

    def select_data(self):
        #db_name = self.tb6.text()
        db_name = self.comboBox.currentText()
        #table_name = self.tb7.text()
        table_name = self.comboBox_2.currentText()

        config = ConfigParser()
        config.read("MyApp_config.ini")
        database = config["mysql_database"]
        db_host = database["host"]
        db_user = database["user"]
        db_password = database["password"]
        try:
            db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_name}")
            cur = db.cursor()
            cur.execute("select * from {}".format(table_name))
            result = cur.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except:
            QMessageBox.information(self, "MyApp", "Invalid DB or Table name!")

    def return_button(self):
        w.setCurrentIndex(3)

class run_log(QDialog):
    def __init__(self):
        super(run_log, self).__init__()

        loadUi("run_aclog.ui", self)
        self.pushButton.clicked.connect(self.parse_drain)
        self.pushButton_2.clicked.connect(self.return_button)
        self.pushButton_3.clicked.connect(self.upload_log_to_database)

    def return_button(self):
        w.setCurrentIndex(3)

    def upload_log_to_database(self):
        upload_log = insert_db.readFile_to_sql('logs')



    def parse_drain(self):

        sys.path.append('./')
        input_dir = self.comboBox_1.currentText()
        output_dir = self.comboBox_1.currentText()
        log_file = self.comboBox_2.currentText()

        log_file_name = log_file.split('_')[0]

        print(log_file_name)

        log_format = self.comboBox_3.currentText()  #'<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>'  # Thunderbird
        regex = self.comboBox_4.currentText()   #[r'(\d+\.){3}\d+']  # Thunderbird
        st = self.spinBox.value()    #.5  # Similarity threshold
        depth = self.doubleSpinBox.value()   #  4  # Depth of all leaf nodes

        benchmark_settings = {
            'HDFS': {
                'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
                'regex': [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'],
            },

            'Hadoop': {
                'log_format': '<Date> <Time> <Level> \[<Process>\] <Component>: <Content>',
                'regex': [r'(\d+\.){3}\d+'],
            },

            'Spark': {
                'log_format': '<Date> <Time> <Level> <Component>: <Content>',
                'regex': [r'(\d+\.){3}\d+', r'\b[KGTM]?B\b', r'([\w-]+\.){2,}[\w-]+'],
            },

            'Zookeeper': {
                'log_format': '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>',
                'regex': [r'(/|)(\d+\.){3}\d+(:\d+)?'],
            },

            'BGL': {
                'log_format': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>',
                'regex': [r'core\.\d+'],
            },

            'HPC': {
                'log_format': '<LogId> <Node> <Component> <State> <Time> <Flag> <Content>',
                'regex': [r'=\d+'],
            },

            'Thunderbird': {
                'log_format': '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>',
                'regex': [r'(\d+\.){3}\d+'],
            },

            'Windows': {
                'log_format': '<Date> <Time>, <Level>                  <Component>    <Content>',
                'regex': [r'0x.*?\s'],
            },

            'Linux': {
                'log_format': '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>',
                'regex': [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}'],
            },

            'Andriod': {
                'log_format': '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>',
                'regex': [r'(/[\w-]+)+', r'([\w-]+\.){2,}[\w-]+',
                          r'\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b'],
            },

            'HealthApp': {
                'log_format': '<Time>\|<Component>\|<Pid>\|<Content>',
                'regex': [],
            },

            'Apache': {
                'log_format': '\[<Time>\] \[<Level>\] <Content>',
                'regex': [r'(\d+\.){3}\d+'],
            },

            'Proxifier': {
                'log_format': '\[<Time>\] <Program> - <Content>',
                'regex': [r'<\d+\ssec', r'([\w-]+\.)+[\w-]+(:\d+)?', r'\d{2}:\d{2}(:\d{2})*', r'[KGTM]B'],
            },

            'OpenSSH': {
                'log_format': '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>',
                'regex': [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+'],
            },

            'OpenStack': {
                'log_format': '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>',
                'regex': [r'((\d+\.){3}\d+,?)+', r'/.+?\s', r'\d+'],
            },

            'Mac': {
                'log_format': '<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>',
                'regex': [r'([\w-]+\.){2,}[\w-]+'],
            },
        }



        start_time = datetime.now()
        parser = aclog.LogParser(log_format=benchmark_settings[log_file_name]['log_format'], indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=benchmark_settings[log_file_name]['regex'])
        parser.parse(log_file)
        time = datetime.now() - start_time

        self.textEdit.setPlainText(log_file+'Parsing done, runtime:' + str(time))

class show_loacl_log(QtWidgets.QMainWindow):

    def __init__(self):
        super(show_loacl_log,self).__init__()
        self.setupUi(self)



    def return_button(self):
        w.setCurrentIndex(3)

    def upload(self):

        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, '选择LOG', './', 'LOG (*.log);')

        print(filetype, filename)

        # 文件不为空则读取文件
        if filename:
            with open(filename, 'r') as fp:
                text = fp.read()
                # 先清空 后赋值
                self.plainTextEdit.setPlainText("")
                self.plainTextEdit.setPlainText(text)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)  # 主窗口大小
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 80, 141, 61))
        self.pushButton.setObjectName("pushButton")

        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(0, 0, 75, 23))
        self.pushButton1.setObjectName("pushButton1")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(220, 30, 391, 281))
        self.groupBox.setObjectName("groupBox")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 30, 351, 211))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.groupBox.raise_()
        self.pushButton.raise_()
        self.pushButton1.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 18))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.upload)
        self.pushButton1.clicked.connect(MainWindow.return_button)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Load file"))
        self.pushButton1.setText(_translate("MainWindow", "Return"))
        self.groupBox.setTitle(_translate("MainWindow", "Log content"))

class main_app(QDialog):
    def __init__(self):
        super(main_app, self).__init__()
        loadUi("main_app.ui", self)

        self.pushButton_1.clicked.connect(self.load_file_page)
        self.pushButton_2.clicked.connect(self.run_log_page)
        self.pushButton_3.clicked.connect(self.database_show)

    def database_show(self):
        w.setCurrentIndex(2)

    def load_file_page(self):
        w.setCurrentIndex(4)

    def run_log_page(self):
        w.setCurrentIndex(5)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QtWidgets.QStackedWidget()
    w_0 = main_app()
    w_1 = show_loacl_log()
    w_2 = run_log()


    w.setWindowTitle("aclog")
    loginform = LoginApp()
    registrationform = RegApp()
    selectform = show_database_log()

    w.addWidget(loginform)
    w.addWidget(registrationform)
    w.addWidget(selectform)
    w.addWidget(w_0)
    w.addWidget(w_1)
    w.addWidget(w_2)

    w.setCurrentIndex(0)
    w.show()


    sys.exit(app.exec_())
