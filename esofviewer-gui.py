from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time as time_
import threading
import esoflib
import eula
import sys
import datetime
import os
import default_theme
class Window(QWidget):
    def __init__(self):
        self.threadpool = QThreadPool()
        try:
            setting = open('esofviewer-cfg/setting.cfg','r')
        except FileNotFoundError:
            try:
                os.mkdir('esofviewer-cfg')
            except:
                pass
            setting = open('esofviewer-cfg/setting.cfg', 'w')
            setting.write('0,None')
            setting.close()
            setting = open('esofviewer-cfg/setting.cfg','r')
        setting = setting.read().split(',')
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setWindowTitle("EBS온라인클래스 뷰어 v0.3b")
        def btn(label,value,ontoggle,ypos,xpos,objname,checkable,checked):
            button = self.button_s = QPushButton(label, objectName=objname)
            button.value = value
            button.setCheckable(checkable)
            button.setChecked(checked)
            button.clicked.connect(ontoggle)
            layout.addWidget(button,ypos,xpos)
        def labeltag(labeltxt,ypos,xpos,objname,value):
            label = self.label_s = QLabel(labeltxt,objectName=objname)
            label.value = value
            label.setMaximumWidth(700)
            layout.addWidget(label,ypos,xpos)
        def textbox(value,ypos,xpos,objname):
            textbox= self.textbox_s = QLineEdit(self,objectName=objname)
            textbox.value = value
            textbox.setMinimumWidth(500)
            layout.addWidget(textbox,ypos,xpos)
        def combobox(items,objname,ypos,xpos):
            combo = self.combo_s = QComboBox(self,objectName=objname)
            combo.addItems(items)
            layout.addWidget(combo,ypos,xpos)
        def plaintext(value,ypos,xpos,objname):
            ptxt = self.ptxt_s = QPlainTextEdit(self,objectName=objname)
            ptxt.insertPlainText(value)
            ptxt.setMinimumWidth(700)
            ptxt.setMinimumHeight(500)
            ptxt.setReadOnly(True)
            layout.addWidget(ptxt,ypos,xpos)
        def checkbox(value,ypos,xpos,objname):
            cbox = self.cbox_s = QCheckBox(self,objectName=objname)
            cbox.setText(value)
            layout.addWidget(cbox,ypos,xpos)
        self.setLayout(layout)
        if setting[0] == '0':
            labeltag('이용 약관 동의',0,0,'EULA','이용 약관 동의')
            plaintext(eula.gpl,1,0,'gpl')
            checkbox('본인은 위 약관을 완벽히 이해하였으며, 동의합니다',2,0,'gplagree')
            checkbox('본인은 해당 소프트웨어를 사용함으로서 발생하는 모든 불이익은 본인 책임임을 이해하며, 동의합니다.',3,0,'noguranteeagree')
            btn('시작','시작',self.agree,4,0,'start',True,False)
        elif setting[0] == '1':
            labeltag('수강 예약(시)',0,0,'lessontimehr','수강예약(시)')
            labeltag('수강 예약(분)',0,1,'lessontimemin','수강예약(분)')
            labeltag('배속',0,2,'playbackspeedlabel','배속')
            labeltag('강의 다운로드',0,3,'downloadlabel','영상 다운로드')
            labeltag('URL',0,4,'urllabel','URL')
            labeltag('강의 시간',0,5,'playbackspeedlabel','강의 시간')
            for i in range(8):
                combobox(['now','00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],'lecthr'+str(i),i*2+1,0)
                minlist = []
                for q in range(60):
                    if len(str(q)) == 1:
                        minlist.append('0'+str(q))
                    else:
                        minlist.append(str(q))
                combobox(minlist,'lectmin'+str(i),i*2+1,1)
                combobox(['1','1.5','20','inf'],'lectspeed'+str(i),i*2+1,2)
                combobox(['X','O'],'lectdl'+str(i),i*2+1,3)
                textbox('',i*2+1,4,'lecturl'+str(i))
                labeltag('0:00',i*2+1,5,'lecttime'+str(i),'0:00')
                labeltag('강의 이름: -----',i*2+2,4,'lectname'+str(i),'')
                labeltag('수강 미완료',i*2+2,5,'lectfin'+str(i),'')
            labeltag('JSESSIONID',19,3,'jsessionid','')
            labeltag('khanuser',20,3,'khanuser','')
            textbox('',19,4,'jsessionid')
            textbox('',20,4,'khanuser')
            btn('시작','시작',self.start,21,4,'start',True,False)
            checkbox('자동시간표',21,3,'autotime')
    def agree(self):
        gpla = self.findChild(QCheckBox, 'gplagree').isChecked()
        nga = self.findChild(QCheckBox, 'noguranteeagree').isChecked()
        if gpla and nga:
            f = open('esofviewer-cfg/setting.cfg','w')
            f.write('1,None')
            f.close()
            self.close()
    def start(self):
        self.findChild(QPushButton, 'start').setText('Fetching Lecture Data')
        self.findChild(QPushButton, 'start').setEnabled(False)
        jsessionid = self.findChild(QLineEdit, 'jsessionid').text()
        khanuser = self.findChild(QLineEdit, 'khanuser').text()
        print(jsessionid)
        lectdata = []
        for i in range(8):
            lecturl = self.findChild(QLineEdit, 'lecturl'+str(i)).text()
            if lecturl == '':
                break
            lecthr = self.findChild(QComboBox, 'lecthr'+str(i)).currentText()
            lectmin = self.findChild(QComboBox, 'lectmin'+str(i)).currentText()
            lectspeed = self.findChild(QComboBox, 'lectspeed'+str(i)).currentText()
            lectdl = self.findChild(QComboBox, 'lectdl'+str(i)).currentText()
            lectdata.append([lecthr + ':' +lectmin,lectspeed, lecturl, lectdl])
        fetchresult = []
        if len(lectdata) == 0:
            self.findChild(QPushButton, 'start').setText('시작')
            self.findChild(QPushButton, 'start').setEnabled(True)
        for i in lectdata:
            print(i)
            try:
                fetchresult.append(esoflib.work(i[2],jsessionid,khanuser,i[1],False,True))
            except Exception as e:
                messagebox = QMessageBox(QMessageBox.Warning, "오류 발생!", "URL,JSESSIONID,khanuser필드를 확인해주세요 \n\n\n\n\n\n 에러코드: {0}".format(e), 
                objectName="errorfetch")
                messagebox.addButton(QPushButton('확인'), QMessageBox.YesRole)
                messagebox.exec_()
                lectdata = []
                fetchresult = []
                self.findChild(QPushButton, 'start').setText('시작')
                self.findChild(QPushButton, 'start').setEnabled(True)
                break
        objid = 0
        plusdelta = datetime.datetime.now()
        for i in fetchresult:
            self.findChild(QLabel, 'lecttime'+str(objid)).setText(i[1]+':'+i[2])
            self.findChild(QLabel, 'lectname'+str(objid)).setText('강의 이름: '+i[0])
            autotime = self.findChild(QCheckBox, 'autotime').isChecked()
            if autotime :
                if objid != 0:
                    #print(i)
                    #print(previ)
                    plusdelta = plusdelta + datetime.timedelta(minutes=int(previ[1])+1)
                    #print(plusdelta.strftime('%H:%M'))
                    idx = self.findChild(QComboBox, 'lecthr'+str(objid)).findText(plusdelta.strftime('%H'), Qt.MatchFixedString)
                    self.findChild(QComboBox, 'lecthr'+str(objid)).setCurrentIndex(idx)
                    idx = self.findChild(QComboBox, 'lectmin'+str(objid)).findText(plusdelta.strftime('%M'), Qt.MatchFixedString)
                    self.findChild(QComboBox, 'lectmin'+str(objid)).setCurrentIndex(idx)
                else:
                    idx = self.findChild(QComboBox, 'lecthr'+str(objid)).findText(plusdelta.strftime('%H'), Qt.MatchFixedString)
                    self.findChild(QComboBox, 'lecthr'+str(objid)).setCurrentIndex(idx)
                    idx = self.findChild(QComboBox, 'lectmin'+str(objid)).findText(plusdelta.strftime('%M'), Qt.MatchFixedString)
                    self.findChild(QComboBox, 'lectmin'+str(objid)).setCurrentIndex(idx)
                lectdata = []
                for q in range(8):
                    lecturl = self.findChild(QLineEdit, 'lecturl'+str(q)).text()
                    if lecturl == '':
                        break
                    lecthr = self.findChild(QComboBox, 'lecthr'+str(q)).currentText()
                    lectmin = self.findChild(QComboBox, 'lectmin'+str(q)).currentText()
                    lectspeed = self.findChild(QComboBox, 'lectspeed'+str(q)).currentText()
                    lectdl = self.findChild(QComboBox, 'lectdl'+str(q)).currentText()
                    lectdata.append([lecthr + ':' +lectmin,lectspeed, lecturl, lectdl])
            previ = i
            objid = objid + 1
        def scheduled(time,url,jsessionid,khanuser,playbackspeed,download,thrid):
            if download == 'O':
                downloadbool = True
            else:
                downloadbool = False
            def esofwrap(url,jsessionid,khanuser,playbackspeed,download,thrid):
                self.findChild(QLabel, 'lectfin'+str(thrid)).setText('수강중')
                print(thrid)
                esoflib.work(url,jsessionid,khanuser,playbackspeed,download)
                self.findChild(QLabel, 'lectfin'+str(thrid)).setText('수강완료')
            if 'now' in time:
                esofwrap(url,jsessionid,khanuser,playbackspeed,downloadbool,thrid)
                return
            else:
                while True:
                    if time == str(datetime.datetime.now().strftime('%H:%M')):
                        esofwrap(url,jsessionid,khanuser,playbackspeed,downloadbool,thrid)
                        return
                    else:
                        print('check')
                        time_.sleep(60)
        thrs = []
        thrid = 0
        for i in lectdata:
            if thrid != 0:
                if i[0].split(':')[0] == 'now':
                    self.findChild(QPushButton, 'start').setText('시작')
                    self.findChild(QPushButton, 'start').setEnabled(True)
                    lectdata = []
                    thrs = []
                    break
            print(i)
            thrs.append(threading.Thread(target=scheduled, args=(i[0], i[2], jsessionid, khanuser, i[1], i[3], thrid)))
            thrid = thrid+1
        for i in thrs:
            i.start() 
        if lectdata != []:
            self.findChild(QPushButton, 'start').setText('Finished!')
app = QApplication(sys.argv)
try:
    css = open('esofviewer-cfg/default.css','r')
except FileNotFoundError:
    try:
        os.mkdir('esofviewer-cfg')
    except Exception:
        pass
    css = open('esofviewer-cfg/default.css','w')
    css.write(default_theme.theme)
    css.close()
app.setStyleSheet(open('esofviewer-cfg/default.css','r').read())
screen = Window()
screen.show()
sys.exit(app.exec_())