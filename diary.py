from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QTime
from subprocess import Popen
import sys, re
import datetime



#time 관련해서는 스레드 문제로 오류나면 무조거 팅김 이제보니까 pyqt는 에러나면 무조건 팅기는거같음
path = 'D:/diary/contents'


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1080, 800)

        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(540, 20, 520, 750))
        self.tabWidget.setObjectName("tabWidget")

         #많은태그순  탭
        self.tabWidgetPage = QtWidgets.QWidget()
        self.tabWidgetPage.setObjectName("tabWidgetPage")
        self.tabWidget.addTab(self.tabWidgetPage, " 태그순 ")
        self.list = QtWidgets.QListView()
        self.tabWidgetPage.layout = QtWidgets.QVBoxLayout()
        self.tabWidgetPage.layout.addWidget(self.list)
        self.tabWidgetPage.setLayout(self.tabWidgetPage.layout)
        self.tag_freq()
        self.list.clicked[QtCore.QModelIndex].connect(self.listclick)


        #최근탭
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage2")
        self.tabWidget.addTab(self.tabWidgetPage1, " 최근 ")
        self.list1 = QtWidgets.QListView()
        self.tabWidgetPage1.layout = QtWidgets.QVBoxLayout()
        self.tabWidgetPage1.layout.addWidget(self.list1)
        self.tabWidgetPage1.setLayout(self.tabWidgetPage1.layout)
        self.recent()
        self.list1.clicked[QtCore.QModelIndex].connect(self.listclick1)

        #검색탭
        self.tabWidgetPage2 = QtWidgets.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.tabWidget.addTab(self.tabWidgetPage2, " 검색 ")
        self.tabWidgetPage2.layout = QtWidgets.QVBoxLayout()
        self.tabWidgetPage2.setLayout(self.tabWidgetPage2.layout)
        self.list2 = QtWidgets.QListView()
        self.tabWidgetPage2.layout.addWidget(self.list2)
        self.list2.clicked[QtCore.QModelIndex].connect(self.listclick1)

#-----------------------------------------------------------------------
        self.pushButton_1 = QtWidgets.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(20, 40, 80, 30))
        self.pushButton_1.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(120, 40, 400, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 120, 500, 510))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 650, 500, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 700, 500, 70))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 80, 500, 30))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        self.pushButton_1.clicked.connect(self.clicksearch)
        self.pushButton_2.clicked.connect(self.clicksave)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_1.setText(_translate("Dialog", "검색"))
        self.pushButton_2.setText(_translate("Dialog", "입력"))

    #태그순 눌렀을때
    def listclick(self,index:QtCore.QModelIndex):
        self.label.setText(index.data())

    # 최근
    def listclick1(self, index:QtCore.QModelIndex):
        path = "D:/diary/contents/"+index.data().rstrip('\n')+".txt"
        self.label.setText(path[18:]+"를 열었다")
        Popen(["notepad",path])

     #검색버튼을 눌렀을때
    def clicksearch(self):
        f = open("D:/diary/list.txt","r")
        data = []
        li = []
        for i in f.readlines():
            li.append(i)
            data.append(i.split())
        f.close()
        li.reverse()
        data.reverse()
        tag = self.lineEdit.text()
        self.lineEdit.clear()
        model3 = QtGui.QStandardItemModel(self.list2)
        for i in range(len(data)):
            for a in range((len(data[i]))):
                if tag == data[i][a]:
                    item = QtGui.QStandardItem(li[i])
                    model3.appendRow(item)
        self.list2.setModel(model3)

    #저장버튼을 눌렀을때
    def clicksave(self):
        content = self.textEdit.toPlainText()
        tag =  self.lineEdit_2.text()
        date = QDateTime.currentDateTime().toString('yyyyMMddhhmmss')
        tag1 = date+" "+tag
        if len(content) == 0:
            self.label.setText("내용을입력해라")
        else:
            f = open(path +"/"+tag+".txt",'w')
            f.write(content)
            f.close()
            self.label.setText(tag+" 저장했다")
            f = open("D:/diary/list.txt","a")
            f.write("'"+tag1+"\n"+"'")
            f.close

        self.lineEdit_2.clear()
        self.textEdit.clear()

    #태그빈도순으로 탭에 정렬
    def tag_freq(self):
        data = []
        words = []
        word_freqs = []
        with open("D:/diary/list.txt","r") as f:
            data = data + list(f.read())
            data_str = ''.join(data)
            words = words + data_str.split()
            for w in words:
                keys = [wd[0] for wd in word_freqs]
                if w in keys:
                    word_freqs[keys.index(w)][1] += 1
                else:
                    word_freqs.append([w, 1])
            word_freqs.sort(key=lambda x: x[1], reverse=True)
            model = QtGui.QStandardItemModel(self.list)
            for i in word_freqs[0:30]:
                tag1 = str(i[0])
                tag2 = str(i[1])
                tag = "#" + tag1 + "  " + tag2 + "번"
                item = QtGui.QStandardItem(tag)
                model.appendRow(item)
        self.list.setModel(model)

    #최근순으로 탭에정렬
    def recent(self):
        li = []
        f = open("D:/diary/list.txt","r")
        for i in f.readlines():
            li.append(i)
        f.close()
        li.reverse()
        model1 = QtGui.QStandardItemModel(self.list1)
        for i in li:
            item = QtGui.QStandardItem(i)
            model1.appendRow(item)
        self.list1.setModel(model1)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
