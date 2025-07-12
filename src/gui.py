import os
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from parseddit import parseddit, options

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = self.build_widget()
        self.setWindowTitle("Reddit Image Parser")

# Sections of the GUI

    def build_widget(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addStretch()
        
        self.input_url = QtWidgets.QLineEdit("")
        self.input_url.setPlaceholderText("Post URL")
        self.input_url.setClearButtonEnabled(True)

        layout.addWidget(self.input_url)
        layout.addStretch()
        layout.addWidget(self.build_options())
        layout.addStretch()
        layout.addLayout(self.build_footer())

        return layout

    def build_footer(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.start_pushbutton = QtWidgets.QPushButton("Start")
        self.start_pushbutton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.start_pushbutton.clicked.connect(self.on_start_clicked)
        self.cancel_pushbutton = QtWidgets.QPushButton("Cancel")
        self.cancel_pushbutton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.cancel_pushbutton.clicked.connect(self.on_cancel_clicked)

        layout.addWidget(self.start_pushbutton)
        layout.addWidget(self.cancel_pushbutton)

        return layout

    def build_options(self):
        box = QtWidgets.QGroupBox("Options")
        
        input_ouputfolder = self.build_filepicker()
        input_foldername = self.build_generic_textinput("Folder Name", "", disabled=False)
        input_overwrite = self.build_generic_checkbox("Overwrite Output", checked=True)
        

        self.selected_folder = input_foldername  # Text input for selected folder
        self.overwrite = input_overwrite
        

        layout = QtWidgets.QVBoxLayout(box)
        layout.setSpacing(20)
        layout.addLayout(input_ouputfolder)
        layout_row1 = QtWidgets.QHBoxLayout(box)
        layout_row1.addWidget(input_overwrite)
        layout_row1.addWidget(input_foldername)
        
        layout.addLayout(layout_row1)

        return box
    
# Components for the GUI

    def build_generic_textinput(self, placeholder, value="", disabled=False):
        text_input = QtWidgets.QLineEdit(value)
        text_input.setPlaceholderText(placeholder)

        text_input.setClearButtonEnabled(not disabled)
        text_input.setDisabled(disabled)

        return text_input  
    def build_generic_checkbox(self, label, checked=True):
        chk_input = QtWidgets.QCheckBox(label)
        chk_input.setChecked(checked)

        return chk_input
    def build_filedialog(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("Select Output Folder")
        dialog.setDirectory(QtCore.QDir.homePath()) 

        return dialog
    def build_filepicker(self):
        self.file_picker = QtWidgets.QPushButton("Pick Folder")
        self.file_picker.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        def_desktop = os.path.expanduser("~/Desktop")
        self.input_ouputfolder = self.build_generic_textinput("Output Folder", def_desktop, disabled=True)
        self.file_picker.clicked.connect(self.on_filepicker_clicked)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.input_ouputfolder)
        layout.addWidget(self.file_picker)
        return layout

# Actions and Slots

    @QtCore.Slot()
    def on_filepicker_clicked(self):
        dialog = self.build_filedialog()
        if dialog.exec():
            selected_folder = dialog.selectedFiles()[0]
            # Here you would typically set the selected folder to a text input or similar
            print(f"Selected folder: {selected_folder}")
            self.input_ouputfolder.setText(selected_folder)

    @QtCore.Slot()
    def on_start_clicked(self):
        self.start_pushbutton.setDisabled(True)

        print(len(self.input_ouputfolder.text()))

        opt = options(
            self.input_url.text(),
            self.input_ouputfolder.text(),
            self.overwrite.isChecked(),
            self.selected_folder.text()
        )

        parser = parseddit(self.input_url.text(), opt)
        parser.parse()

        self.close()

    @QtCore.Slot()
    def on_cancel_clicked(self):
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(600, 1)
    widget.show()

    sys.exit(app.exec())