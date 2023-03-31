import os
import re
from PyQt5.QtWidgets import QDialog, QLabel, QWidget,QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy,QTextEdit, QShortcut,QLineEdit, QMenu, QAction,QFileDialog

from PyQt5.QtGui import QIcon, QFont,QKeySequence
from PyQt5.QtCore import Qt,QEvent,QTimer

class MyDialog(QDialog):
    def __init__(self, options,title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.files = []
        self.folders = []
        # Create the label and combo box for the options
        options_label = QLabel("To:")
        self.options_combo = QComboBox()
        self.options_combo.setEditable(True)
        self.options_combo.addItems(options)
        self.options_combo.setInsertPolicy(QComboBox.InsertAtBottom)

        # Create the text edit for the message
        self.message_edit = QTextEdit()
        self.message_edit.setPlaceholderText("Enter message or drag and drop files here, use ctlr+enter to send message")
        # self.message_edit.setDragEnabled(True)
        self.message_edit.setAcceptDrops(True)
        self.message_edit.installEventFilter(self)
        
        # Create the send button
        self.send_button = QPushButton("Send")
        self.send_button.setDefault(True)

        # Create the layout
        options_layout = QHBoxLayout()
        options_layout.addWidget(options_label)
        options_layout.addWidget(self.options_combo)

        message_layout = QVBoxLayout()
        message_layout.addWidget(self.message_edit)
        message_layout.addWidget(self.send_button)

        layout = QVBoxLayout()
        layout.addLayout(options_layout)
        layout.addLayout(message_layout)

        # Set the layout
        self.setLayout(layout)

        # Connect the signals and slots
        self.send_button.clicked.connect(self.accept)
        self.shortcut = QShortcut(QKeySequence('Ctrl+Return'), self)
        self.shortcut.activated.connect(self.accept)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)


        self.message_edit.textChanged.connect(self.handleTextChanged)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.handleTimerTimeout)  

        self.pathWidget = QWidget()
        self.pathLayout = QVBoxLayout()
        self.pathLabel = QLabel("Files Attached:")
        self.pathListLabel = QLabel()
        self.pathLayout.addWidget(self.pathLabel)
        self.pathLayout.addWidget(self.pathListLabel)
        self.pathWidget.setLayout(self.pathLayout)
        self.pathWidget.hide()  
    
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
            # self.message_edit.setText("\n".join(self.files))

    def insert_folder(self):
        folder_dialog = QFileDialog(self, "Select Folder")
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if folder_dialog.exec_():
            folder_path = folder_dialog.selectedFiles()[0]
            self.folders.append(folder_path)
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
        # matches = re.findall(r"file:///\S+", text)
        # pat                 =r"file:///[-\w,\s/\\:]+\.[A-Za-z0-9.]{1,11}|file:///[-\w,\s/\\:]+\S"
        matches = re.findall(r"file:///[-\w,\s/\\:]+\.[A-Za-z0-9.]{1,11}|file:///[-\w,\s/\\:]+\S", text)
        if len(matches)!=0:
            for match in matches:
                path = match.replace("file:///", "")
                if os.path.isfile(path):
                    self.files.append(path)
                elif os.path.isdir(path):
                    self.folders.append(path)
                text = text.replace(match, '')
            self.message_edit.setPlainText(text)

        if self.files or self.folders:
            ad="\n".join(self.files)+"\n".join(self.folders)
            self.pathListLabel.setText(ad)
            self.pathWidget.show()
        

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
print(a,b,c,d)