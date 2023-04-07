import os
import re
from PyQt5 import uic
# from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont,QKeySequence
from PyQt5.QtCore import Qt,QEvent,QTimer,QRect
from PyQt5.QtWidgets import *

#%%# Form, Window = uic.loadUiType("msg-send.ui")
class MyDialog(QDialog):
    def __init__(self, options,title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.files = []
        self.folders = []

        menuBar = QMenuBar(self)

        uic.loadUi("msg.ui",self)

        self.llayout.addWidget(menuBar)
        # Create a new menu and add it to the menu bar
        fileMenu = menuBar.addMenu('&Menu')

        # Create new menu items and add them to the menu
        newAction = QAction('&Add Files', self)
        newAction.setShortcut('Ctrl+I')
        newAction.triggered.connect(self.insert_file)
        fileMenu.addAction(newAction)

        openAction = QAction('&Add Folders', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.insert_folder)
        fileMenu.addAction(openAction)

        saveAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        fileMenu.addAction(saveAction)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)



        self.options_combo.addItems(options)
        self.message_edit.installEventFilter(self)
        self.listView.hide()
        self.pathLabel.hide()

        self.send_button.clicked.connect(self.accept)
        self.shortcut = QShortcut(QKeySequence('Ctrl+Return'), self)
        self.shortcut.activated.connect(self.accept)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)


        self.message_edit.textChanged.connect(self.handleTextChanged)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.handleTimerTimeout) 
    
       
    
    
    
    def show_context_menu(self, point):
        menu = QMenu(self)
        add_file_action = menu.addAction("Add File")
        add_folder_action = menu.addAction("Add Folder")
        action = menu.exec_(self.mapToGlobal(point))
        if action == add_file_action:
            self.insert_file()
            # self.add_file()
        elif action == add_folder_action:
            # self.add_folder()
            self.insert_folder()


    def insert_file(self):
        file_dialog = QFileDialog(self, "Select File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.files.append(file_path)
        if self.files or self.folders:
            ad="\n".join(self.files)+"\n".join(self.folders)
            self.listView.setText(ad)
            self.pathLabel.show()
            self.listView.show()
            # self.message_edit.setText("\n".join(self.files))

    def insert_folder(self):
        folder_dialog = QFileDialog(self, "Select Folder")
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if folder_dialog.exec_():
            folder_path = folder_dialog.selectedFiles()[0]
            self.folders.append(folder_path)
        if self.files or self.folders:
            ad="\n".join(self.files)+"\n".join(self.folders)
            self.listView.setText(ad)
            self.pathLabel.show()
            self.listView.show()
            # self.message_edit.setText("\n".join(self.folders))


    def message(self):
        # Return the message
        return self.message_edit.toPlainText()

    def selected_option(self):
        # Return the selected option
        return self.options_combo.currentText()
    def handleTextChanged(self):
        self.timer.start(500) 
    
    def handleTimerTimeout(self):
        text = self.message_edit.toPlainText()
        matches = re.findall(r"file:///[-\w,\s/\\:]+\.[A-Za-z0-9.]{1,11}|file:///[-\w,\s/\\:]+\S", text)
        if len(matches)!=0:
            for match in matches:
                path = match.replace("file:///", "")
                if os.path.isfile(path):
                    self.files.append(path)
                elif os.path.isdir(path):
                    self.folders.append(path)
                try:
                    text = text.replace(match+'\n', '')
                except:
                    text = text.replace(match, '')
            self.message_edit.setPlainText(text)

        if self.files or self.folders:
            ad="\n".join(self.files)+"\n".join(self.folders)
            self.listView.setText(ad)
            self.pathLabel.show()
            self.listView.show()
#%%
def message_box(options,title):
    app = QApplication([])
    dialog = MyDialog(options,title)
    result = dialog.exec_()
    if result == QDialog.Accepted:
        return dialog.message(), dialog.selected_option(),dialog.files,dialog.folders
    else:
        return None, None,None,None
    
country_names = ["Argentina", "Brazil", "Canada", "Denmark", "Egypt", "France", "Germany", "Honduras", "India", "Japan", "Kenya", "Liberia", "Mexico", "Nigeria", "Oman", "Peru", "Qatar", "Russia", "Spain", "Thailand", "United States", "Vietnam", "Yemen", "Zimbabwe"]
a,b,c,d=0,0,0,0
# b,a=message_box(country_names,"Send Message" )
b,a,d,c=message_box(country_names,"Send Message" )
# print(dir(message_box))
print(a,b,c,d)

