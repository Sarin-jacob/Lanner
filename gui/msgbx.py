
#%%
import os
import re
from PyQt5.QtWidgets import QDialog, QLabel, QWidget,QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy,QTextEdit, QShortcut, QMenu, QFileDialog

from PyQt5.QtGui import QIcon, QFont,QKeySequence
from PyQt5.QtCore import Qt,QEvent,QTimer

#%%
class MyMessageBox(QDialog):
    def __init__(self, message, title,icon, parent=None):
        super(MyMessageBox, self).__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon))
        self.files = []
        self.folders = []
        
        # Message Label
        self.messageLabel = QLabel(message)
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.messageLabel.setFont(QFont('Arial', 12))
        self.messageLabel.setMaximumWidth(800)
        self.messageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.messageLabel.setWordWrap(True)

        #testing
        self.setAcceptDrops(True)
        self.installEventFilter(self)

        
        
        
        # Input Label and Input Box
        self.inputLabel = QLabel("Reply:")
        self.inputInput = QTextEdit()
        self.inputInput.setMinimumHeight(40)
        self.inputInput.setMaximumHeight(40)
        self.inputInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputInput.setPlaceholderText("Enter message or drag and drop files here, use ctlr+enter to send message")
        # self.inputInput.setDragEnabled(True)
        self.inputInput.setAcceptDrops(True)
        # self.inputInput.installEventFilter(self)

        self.inputInput.textChanged.connect(self.handleInputChanged)

        self.inputInput.textChanged.connect(self.handleTextChanged)
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
        

        self.inputLayout = QVBoxLayout()
        self.inputLayout.addWidget(self.inputLabel)
        self.inputLayout.addWidget(self.inputInput)
        # print(self.inputInput.sizeHint())
        # OK Button
        self.okButton = QPushButton("Send")
        self.okButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.okButton.clicked.connect(self.handleOkClicked)
        
        # Button Layout
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.okButton, alignment=Qt.AlignCenter)
        self.buttonLayout.addStretch(1)
        
        # Main Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.messageLabel)
        vbox.addLayout(self.inputLayout)
        vbox.addLayout(self.buttonLayout)
        self.setLayout(vbox)
        
        # Ensure the dialog is big enough to show the entire title
        self.adjustSize()
        titleWidth = len(title)*12 + 20
        self.setMinimumWidth(max(self.minimumWidth(), titleWidth))

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
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


    def handleInputChanged(self):
        document = self.inputInput.document()
        text_height = document.size().height()
        if self.minimumHeight()<300:
            self.inputInput.setFixedHeight(int(text_height))
            self.setMinimumHeight=self.minimumHeight()+int(text_height)
        # print(self.minimumHeight())
        # self.inputInput.setMinimumHeight(self.inputInput.sizeHint().height())
        
    
    def handleOkClicked(self):
        self.accept()
        
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

    def getResult(self):
        return self.inputInput.toPlainText()
    
    def handleTextChanged(self):
        self.timer.start(500) 
    
    def handleTimerTimeout(self):
        text = self.inputInput.toPlainText()
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
            self.inputInput.setPlainText(text)

        if self.files or self.folders:
            ad="\n".join(self.files)+"\n".join(self.folders)
            self.pathListLabel.setText(ad)
            self.pathWidget.show()


    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Return:
            # Ctrl+Enter was pressed, simulate a click on the OK button
            self.accept()
            # self.okButton.button(QDialogButtonBox.Ok).click()
        else:
            # Call the base class implementation to handle other key events normally
            super().keyPressEvent(event)

    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.DragEnter:
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
        elif event.type() == QEvent.Drop:
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    path = url.toLocalFile()
                    if os.path.isfile(path):
                        self.files.append(path)
                    elif os.path.isdir(path):
                        self.folders.append(path)
                event.acceptProposedAction()
                if self.files or self.folders:
                    ad="\n".join(self.files)+"\n".join(self.folders)
                    self.pathListLabel.setText(ad)
                    self.pathWidget.show()
        # elif obj in (self.file_list, self.folder_list) and event.type() == QEvent.KeyPress:
        #     if event.key() == Qt.Key_Return and event.modifiers() ==Qt.ControlModifier:
        #         self.accept()
        #         return True
        return super().eventFilter(obj, event)


def showMessageBox(message:str, title:str,icon="icon.png"):
    app = QApplication([])
    msgBox = MyMessageBox(message, title,icon)
    if msgBox.exec_() == QDialog.Accepted:
        return msgBox.getResult(),msgBox.files,msgBox.folders
    else:
        return None,None,None
#%%

class MyDialog(QDialog):
    def __init__(self, options,title,icon, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon))
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
        # self.message_edit.installEventFilter(self)
        
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
        

def message_box(options:list,title:str,icon="icon.png"):
    app = QApplication([])
    dialog = MyDialog(options,title,icon)
    result = dialog.exec_()
    if result == QDialog.Accepted:
        return dialog.message(), dialog.selected_option(),dialog.files,dialog.folders
    else:
        return None, None,None,None



