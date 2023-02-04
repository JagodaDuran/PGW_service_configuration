from PyQt6 import QtWidgets, QtCore,  QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QRadioButton, QGroupBox, QVBoxLayout, QCheckBox
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
import socket
import re


class Servis(QWidget):
    def __init__(self):
        self.filter = b""
        self.action = b""
        self.list = []
        self.edit_dom_ip = None      
        super().__init__()
        # Create a UDS socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_addres = 'unix_sock'
        print("Connecting to server...")
        try:
            self.sock.connect(server_addres)
        except socket.error:
            print("Error while connecting on server...")
            sys.exit(1)

        self.setupui()

    def setupui(self):
        self.resize(1500, 800)
        self.setWindowTitle("Python Application")
        self.setWindowIcon(QIcon("./python/img/server_icon.png"))

        id1 = QFontDatabase.addApplicationFont(
            "./python/fonts/Blox2.ttf")
        if id1 < 0:
            print("Error")
        families = QFontDatabase.applicationFontFamilies(id1)
        print(families[0])

        self.label_title1 = QLabel("PGW", self)
        self.label_title1.setFont(QFont("Blox BRK", 30))

        id2 = QFontDatabase.addApplicationFont(
            "./python/fonts/ROBOTECH_GP.ttf")
        if id2 < 0:
            print("Error")
        families = QFontDatabase.applicationFontFamilies(id2)
        print(families[0])

        self.label_title2 = QLabel("Automatic Service Configuration", self)
        self.label_title2.setFont(QFont("ROBOTECH GP", 30))

        # --------------------------Image section-------------------------------------------

        pixmap_image1 = QPixmap(
            "./python/img/abstract.jpg")
        pixmap_image2 = pixmap_image1.scaled(50, 50)

        self.label_pixmap1 = QLabel()
        self.label_pixmap1.setPixmap(pixmap_image2)

        hbox_image = QHBoxLayout()
        hbox_image.addWidget(self.label_pixmap1)
        hbox_image.addWidget(self.label_title1, Qt.AlignmentFlag.AlignLeft)

        hbox_title2 = QVBoxLayout()
        hbox_image.addWidget(self.label_title2, Qt.AlignmentFlag.AlignBottom)

        # --------------------------Service info---------------------------------------------------

        self.groupbox_service_info = QGroupBox("Service Info")

        self.label_servicename = QLabel("Service name")
        self.edit_servicename = QLineEdit()
        self.list.append(self.edit_servicename)
        self.edit_servicename.setPlaceholderText(
            "Enter a maximum of 10 characters...")
        self.edit_servicename.setValidator
        self.regexp_name = QtCore.QRegularExpression("^[a-zA-Z0-9_]*$")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp_name)
        self.edit_servicename.setValidator(self.validator)
        self.edit_servicename.setMaxLength(10)

        self.label_mkey = QLabel("Monitoring key")
        self.edit_mkey = QLineEdit()
        self.list.append(self.edit_mkey)
        self.edit_mkey.setPlaceholderText("[1-10 000]")
        self.edit_mkey.setValidator
        # ^ symbol matches the beginning of the string. The first digit is non zero [1-9]
        # Then we can have up to 9 digits.
        self.regexp1 = QtCore.QRegularExpression("^[1-9][0-9]{0,4}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp1)
        self.edit_mkey.setValidator(self.validator)

        self.label_priority_n = QLabel("Priority of normal rule")
        self.edit_priority_n = QLineEdit()
        self.list.append(self.edit_priority_n)
        self.edit_priority_n.setPlaceholderText("[1-100 000]")
        self.edit_priority_n.setValidator
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,5}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp2)
        self.edit_priority_n.setValidator(self.validator)

        self.label_priority_e = QLabel("Priority of exhaust rule")
        self.edit_priority_e = QLineEdit()
        self.list.append(self.edit_priority_e)
        self.edit_priority_e.setPlaceholderText("[1-100 000]")
        self.edit_priority_e.setValidator
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,5}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp2)
        self.edit_priority_e.setValidator(self.validator)

        self.label_rg_n = QLabel("Rating group of normal rule")
        self.edit_rg_n = QLineEdit()
        self.list.append(self.edit_rg_n)
        self.edit_rg_n.setPlaceholderText("[1-10 000]")
        self.edit_rg_n.setValidator
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,4}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp1)
        self.edit_rg_n.setValidator(self.validator)

        self.label_rg_e = QLabel("Rating group of exhaust rule")
        self.edit_rg_e = QLineEdit()
        self.list.append(self.edit_rg_e)        
        self.edit_rg_e.setPlaceholderText("[1-10 000]")
        self.edit_rg_e.setValidator(QIntValidator())
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,4}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp1)
        self.edit_rg_e.setValidator(self.validator)

        self.label_filter = QLabel("Filter")
        self.edit_filter = QLineEdit()

        grid_service_info = QGridLayout()
        grid_service_info.addWidget(self.label_servicename, 0, 0)
        grid_service_info.addWidget(self.edit_servicename, 0, 1)

        grid_service_info.addWidget(self.label_mkey, 1, 0)
        grid_service_info.addWidget(self.edit_mkey, 1, 1)

        grid_service_info.addWidget(self.label_priority_n, 2, 0)
        grid_service_info.addWidget(self.edit_priority_n, 2, 1)

        grid_service_info.addWidget(self.label_priority_e, 3, 0)
        grid_service_info.addWidget(self.edit_priority_e, 3, 1)

        grid_service_info.addWidget(self.label_rg_n, 4, 0)
        grid_service_info.addWidget(self.edit_rg_n, 4, 1)

        grid_service_info.addWidget(self.label_rg_e, 5, 0)
        grid_service_info.addWidget(self.edit_rg_e, 5, 1)

        vbox_service_info = QVBoxLayout()
        vbox_service_info.addLayout(grid_service_info)
        self.groupbox_service_info.setLayout(vbox_service_info)

        # --------------------------Speed Section--------------------------------------------

        self.groupbox_speed = QGroupBox("Speed Section")

        self.label_normal_dw = QLabel("Normal speed downlink in Mb/s")
        self.edit_normal_dw = QLineEdit()
        self.list.append(self.edit_normal_dw)
        self.edit_normal_dw.setPlaceholderText("[1-100 000]")
        self.edit_normal_dw.setValidator
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,5}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp2)
        self.edit_normal_dw.setValidator(self.validator)

        self.label_normal_up = QLabel("Normal speed uplink in Mb/s")
        self.edit_normal_up = QLineEdit()
        self.list.append(self.edit_normal_up)
        self.edit_normal_up.setPlaceholderText("[1-100 000]")
        self.edit_normal_up.setValidator
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,5}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp2)
        self.edit_normal_up.setValidator(self.validator)

        self.label_exhaust_dw = QLabel("Exhaust speed downlink in kb/s")
        self.edit_exhaust_dw = QLineEdit()
        self.list.append(self.edit_exhaust_dw)
        self.edit_exhaust_dw.setPlaceholderText("[1-100 000]")
        self.edit_exhaust_dw.setValidator
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,5}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp2)
        self.edit_exhaust_dw.setValidator(self.validator)

        self.label_exhaust_up = QLabel("Exhaust speed uplink in kb/s")
        self.edit_exhaust_up = QLineEdit()
        self.list.append(self.edit_exhaust_up)
        self.edit_exhaust_up.setPlaceholderText("[1-100 000]")
        self.edit_exhaust_up.setValidator
        self.regexp2 = QtCore.QRegularExpression("^[1-9][0-9]{0,5}")
        self.validator = QtGui.QRegularExpressionValidator(self.regexp2)
        self.edit_exhaust_up.setValidator(self.validator)

        grid_speed = QGridLayout()
        grid_speed.addWidget(self.label_normal_dw, 0, 0)
        grid_speed.addWidget(self.edit_normal_dw, 0, 1)

        vbox_speed = QVBoxLayout()
        vbox_speed.addLayout(grid_speed)
        self.groupbox_speed.setLayout(vbox_speed)

        grid_speed.addWidget(self.label_normal_dw, 1, 0)
        grid_speed.addWidget(self.edit_normal_dw, 1, 1)

        grid_speed.addWidget(self.label_normal_up, 2, 0)
        grid_speed.addWidget(self.edit_normal_up, 2, 1)

        grid_speed.addWidget(self.label_exhaust_dw, 3, 0)
        grid_speed.addWidget(self.edit_exhaust_dw, 3, 1)

        grid_speed.addWidget(self.label_exhaust_up, 4, 0)
        grid_speed.addWidget(self.edit_exhaust_up, 4, 1)

        # --------------------------Filter Section-------------------------------------------

        self.groupbox_filter = QGroupBox("Filter Section")

        self.radio1 = QRadioButton("Filter all trafic")
        self.radio1.toggled.connect(self.func_filter)
        self.radio2 = QRadioButton("Filter tcp trafic")
        self.radio2.toggled.connect(self.func_filter)
        self.radio3 = QRadioButton("Filter udp trafic")
        self.radio3.toggled.connect(self.func_filter)
        self.radio4 = QRadioButton("Filter dns trafic")
        self.radio4.toggled.connect(self.func_filter)

        self.radio5 = QRadioButton("Filter IP")
        self.radio5.toggled.connect(self.func_filter)
        self.radio5.toggled.connect(self.func_radio_IP)

        self.radio6 = QRadioButton("Filter doman name")
        self.radio6.toggled.connect(self.func_filter)
        self.radio6.toggled.connect(self.func_radio_domain_name)

        self.grid_filter = QGridLayout()
        self.grid_filter.addWidget(self.radio1, 0, 0)
        self.grid_filter.addWidget(self.radio2, 1, 0)
        self.grid_filter.addWidget(self.radio3, 2, 0)
        self.grid_filter.addWidget(self.radio4, 3, 0)
        self.grid_filter.addWidget(self.radio5, 4, 0)
        self.grid_filter.addWidget(self.radio6, 5, 0)

        self.vbox_filter = QVBoxLayout()
        self.vbox_filter.addLayout(self.grid_filter)
        self.groupbox_filter.setLayout(self.vbox_filter)

        # --------------------------Action Section-------------------------------------------

        self.groupbox_action = QGroupBox("Action Section")

        self.radio_action1 = QRadioButton("Write rating group into file")
        self.radio_action1.toggled.connect(self.func_action)
        self.radio_action2 = QRadioButton("Implement header enrichment")
        self.radio_action2.toggled.connect(self.func_action)
        self.radio_action3 = QRadioButton("Drop packets")
        self.radio_action3.toggled.connect(self.func_action)

        grid_action = QGridLayout()
        grid_action.addWidget(self.radio_action1, 0, 0)
        grid_action.addWidget(self.radio_action2, 1, 0)
        grid_action.addWidget(self.radio_action3, 2, 0)

        vbox_action = QVBoxLayout()
        vbox_action.addLayout(grid_action)
        self.groupbox_action.setLayout(vbox_action)

        # --------------------------Servis output--------------------------------------------

        self.groupbox_output1 = QGroupBox("Servis output")

        self.text_output1 = QTextEdit()
        self.list.append(self.text_output1)
        self.text_output1.setReadOnly(True)

        vbox_output1 = QHBoxLayout()
        vbox_output1.addWidget(self.text_output1)
        self.groupbox_output1.setLayout(vbox_output1)

        # --------------------------Icon and Button-------------------------------------------

        icon_display = QIcon(
            "./python/img/display_icon.png")
        self.displaybutton = QPushButton("\tSubmit")
        self.displaybutton.setIcon(icon_display)
        self.displaybutton.setFixedSize(90, 30)
        self.displaybutton.clicked.connect(self.func_send_recv_uds)        

        icon_reset = QIcon("./python/img/reset_icon.png")
        self.resetbutton = QPushButton("\tReset")
        self.resetbutton.setIcon(icon_reset)
        self.resetbutton.setFixedSize(90, 30)
        self.resetbutton.clicked.connect(self.func_clear_service)

        icon_exit = QIcon("./python/img/exit_icon.png")
        self.exitbutton = QPushButton("\tExit")
        self.exitbutton.setIcon(icon_exit)
        self.exitbutton.setFixedSize(90, 30)
        self.exitbutton.clicked.connect(self.func_send_termination_uds)
        self.exitbutton.clicked.connect(self.close)

        hbox_addbutton = QHBoxLayout()
        hbox_addbutton.addWidget(
            self.displaybutton, 2, Qt.AlignmentFlag.AlignRight)
        hbox_addbutton.addWidget(self.resetbutton)
        hbox_addbutton.addWidget(self.exitbutton)

        # --------------------------Layout---------------------------------------------------

        layout_hmix1 = QHBoxLayout()
        layout_hmix1.addWidget(self.groupbox_service_info)
        layout_hmix1.addWidget(self.groupbox_speed)
        layout_hmix1.addWidget(self.groupbox_filter)
        layout_hmix1.addWidget(self.groupbox_action)

        layout_vmix1 = QVBoxLayout()
        layout_vmix1.addWidget(self.groupbox_output1)

        layout_vmix2 = QVBoxLayout()
        layout_vmix2.addLayout(hbox_image)
        layout_vmix2.addLayout(hbox_title2)
        layout_vmix2.addLayout(layout_hmix1)
        layout_vmix2.addLayout(layout_vmix1)
        layout_vmix2.addLayout(hbox_addbutton)

        self.setLayout(layout_vmix2)

    def func_send_recv_uds(self):
        
        if self.func_check_input_for_submit() == False:
            self.func_palette()
            return
        
        # --------------------------Socket section client-------------------------------------------
        try:
            b = self.func_text_to_bytes()
            # Send data
            payloadLength = len(b)
            print("Sending message:\n", payloadLength, b)
            self.sock.sendall(payloadLength.to_bytes(4, byteorder='little'))
            self.sock.sendall(b)
        except Exception as ex:
            print("Error while sending data through unix socket!", ex)

        try:
            print("Receiving generated service configuration file...")
            length = int.from_bytes(self.sock.recv(4), "little")
            data = self.sock.recv(length).decode("utf-8")
            self.text_output1.setText(data)
        except Exception as ex:
            print("Error while receiving data through unix socket!", ex)

    def func_send_termination_uds(self):
        # --------------------------Socket section client-------------------------------------------
        terminationPayload = 0
        try:
            print("Terminating connecion with client")
            self.sock.sendall(
                terminationPayload.to_bytes(4, byteorder='little'))
        except:
            print("Error when trying to terminate connection")
        finally:
            self.sock.close()
            print("Socket is closed!")

        # --------------------------GUI---------------------------------------------------

    def func_gui(self):
        return """
        Servis{
            background-color: "lightblue";      
        }     
       """

    def func_filter(self):
        if self.radio1.isChecked():
            self.filter = b"1"
            print(self.filter)

        if self.radio2.isChecked():
            self.filter = b"2"
            print(self.filter)

        if self.radio3.isChecked():
            self.filter = b"3"
            print(self.filter)

        if self.radio4.isChecked():
            self.filter = b"4"
            print(self.filter)

        if self.radio5.isChecked():
            self.filter = b"5"
            print(self.filter)

        if self.radio6.isChecked():
            self.filter = b"6"
            print(self.filter)

    def func_action(self):
        if self.radio_action1.isChecked():
            self.action = b"1"
            print(self.action)

        if self.radio_action2.isChecked():
            self.action = b"2"
            print(self.action)

        if self.radio_action3.isChecked():
            self.action = b"3"
            print(self.action)

    def func_clear_service(self):
        print("List---------------------")
        for item in self.list:
            print(item.clear())        
        
        if hasattr(self.edit_dom_ip, "clear"):
            self.edit_dom_ip.clear() 
        
    def func_text_to_bytes(self):
        payload = b""
        self.text_service_name = self.edit_servicename.text()
        self.bytes_text_service_name = bytes(self.text_service_name, 'utf-8')
        print("Sending service name...\n")
        payload += self.bytes_text_service_name + b";"

        self.text_mkey = self.edit_mkey.text()
        self.bytes_text_mkey = bytes(self.text_mkey, 'utf-8')
        print("Sending monitoring key...\n")
        payload += self.bytes_text_mkey + b";"

        self.text_priority_n = self.edit_priority_n.text()
        self.bytes_text_priority_n = bytes(self.text_priority_n, 'utf-8')
        print("Sending priority of normal rule...\n")
        payload += self.bytes_text_priority_n + b";"

        self.text_priority_e = self.edit_priority_e.text()
        self.bytes_text_priority_e = bytes(self.text_priority_e, 'utf-8')
        print("Sending priority of exhaust rule...\n")
        payload += self.bytes_text_priority_e + b";"

        self.text_rg_n = self.edit_rg_n.text()
        self.bytes_text_rg_n = bytes(self.text_rg_n, 'utf-8')
        print("Sending Rating group for normal rule...\n")
        payload += self.bytes_text_rg_n + b";"

        self.text_rg_e = self.edit_rg_e.text()
        self.bytes_text_rg_e = bytes(self.text_rg_e, 'utf-8')
        print("Sending Rating group for exhaust rule...\n")
        payload += self.bytes_text_rg_e + b";"

        self.text_edit_normal_dw = self.edit_normal_dw.text()
        self.bytes_edit_normal_dw = bytes(self.text_edit_normal_dw, 'utf-8')
        print("Sending downlink speed for normal rule...\n")
        payload += self.bytes_edit_normal_dw + b";"

        self.text_edit_normal_up = self.edit_normal_up.text()
        self.bytes_edit_normal_up = bytes(self.text_edit_normal_up, 'utf-8')
        print("Sending uplink speed for normal rule...\n")
        payload += self.bytes_edit_normal_up + b";"

        self.text_edit_exhaust_dw = self.edit_exhaust_dw.text()
        self.bytes_edit_exhaust_dw = bytes(self.text_edit_exhaust_dw, 'utf-8')
        print("Sending downlink speed for exhaust rule...\n")
        payload += self.bytes_edit_exhaust_dw + b";"

        self.text_edit_exhaust_up = self.edit_exhaust_up.text()
        self.bytes_edit_exhaust_up = bytes(self.text_edit_exhaust_up, 'utf-8')
        print("Sending uplink speed for exhaust rule...\n")
        payload += self.bytes_edit_exhaust_up + b";"

        payload += self.filter
        if self.filter == b"5":
            payload += bytes(self.edit_IP.text(), 'utf-8')

        if self.filter == b"6":
            payload += bytes(self.edit_domain_name.text(), 'utf-8')

        payload += b";"
        payload += self.action + b";"

        return payload

    def func_radio_IP(self):
        if self.radio5.isChecked():            
            self.edit_IP = QLineEdit() 
            self.edit_dom_ip = self.edit_IP                    
            self.edit_IP.setPlaceholderText("Enter IP address...")
            self.grid_filter.addWidget(self.edit_IP, 4, 1)
            self.edit_IP.setValidator
            self.regexp3 = QtCore.QRegularExpression(
                "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
            self.validator = QtGui.QRegularExpressionValidator(self.regexp3)
            self.edit_IP.setValidator(self.validator)
        if hasattr(self,"edit_domain_name") and self.edit_domain_name != None:
            self.grid_filter.removeWidget(self.edit_domain_name)            
            self.edit_domain_name.deleteLater()
            self.edit_domain_name = None

    def func_radio_domain_name(self):
        if self.radio6.isChecked():
            self.edit_domain_name = QLineEdit()  
            self.edit_dom_ip = self.edit_domain_name                    
            self.edit_domain_name .setPlaceholderText(
                "Enter in a form e.g google.com")
            self.grid_filter.addWidget(self.edit_domain_name, 5, 1)
            self.edit_domain_name .setValidator
            self.regexp4 = QtCore.QRegularExpression(
                "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$")
            self.validator = QtGui.QRegularExpressionValidator(self.regexp4)
            self.edit_domain_name.setValidator(self.validator)
            self.edit_domain_name.setMaxLength(10)  
        if hasattr(self,"edit_IP") and self.edit_IP != None:
            self.grid_filter.removeWidget(self.edit_IP)            
            self.edit_IP.deleteLater()
            self.edit_IP = None            

    def func_check_input_for_submit(self):
        for item in self.list:
            if type(item) == type(QLineEdit()) and item.text() == "":                
                return False                         
        return True     

    def func_palette(self): 
        for item in self.list:
            if type(item) == type(QLineEdit()) and item.text() == "":
                text_color = QtGui.QColor("red")
                pal = item.palette()
                pal.setColor(QtGui.QPalette.ColorRole.PlaceholderText, text_color)
                item.setPalette(pal)            
           
            if self.edit_dom_ip != None and self.edit_dom_ip.text() == "":                
                text_color = QtGui.QColor("red")
                pal = self.edit_dom_ip.palette()
                pal.setColor(QtGui.QPalette.ColorRole.PlaceholderText, text_color)
                self.edit_dom_ip.setPalette(pal)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Servis()
    app.setStyleSheet(form.func_gui())
    form.show()
    import time
    app.exec()
