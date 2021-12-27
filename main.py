# coded by: @bluejayws (Antonio G-B), w/help from the internet, stackoverflow, etc.
# icons used are made by: Freepik,
import os
import sys
import subprocess

from PyQt6.QtCore import Qt
# Note to self: This import below is causing me a headache on MacOS (M1 chip). Gonna try to continue this project when I'm back on 
#   my Windows laptop
from preview_generator.manager import PreviewManager
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QHBoxLayout, QWidget, QFileDialog, QPushButton, QVBoxLayout, QCheckBox, QListWidget,
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("💻 Desktop Organizer 🥞")
        self.file_list = []
        # to store the directory path for later use
        self.directory_path_name = "/"
        #________________________LAYOUT INITIALIZATION________________________
        layer_one = QHBoxLayout()  # Select a folder, selected directory
        layer_two = QHBoxLayout()  # Selected directory contents
        layer_three = QHBoxLayout()  # Second line of buttons
        layer_three_vertical_one = QVBoxLayout()  # Store the first column w/checkbox and "Convert"
        layer_three_vertical_two = QVBoxLayout()  # Store the second column w/checkbox and "Open in File Browser"
        vertical_layout_parent = QVBoxLayout()

        #________________________WIDGET INITIALIZATION______________________________
        # Parent widget
        widget = QWidget()

        # Displays "Select a folder" button
        self.select_a_folder_button = QPushButton()
        self.select_a_folder_button.setText("Select a folder:")
        self.select_a_folder_button.clicked.connect(self.select_folder_prompt)
        self.select_a_folder_button.show()

        # Shows selected directory as a String
        self.directory_label = QLabel()
        self.directory_label.setText("Directory to be worked on will show here            ")
        self.directory_label.show()

        # Displays the file contents of the selected folder
        self.file_paths_list_widget = QListWidget()
        self.file_paths_list_widget.show()
        # self.file_paths_list_widget.itemClicked.connect(self.print_item_clicked)
        self.file_paths_list_widget.itemSelectionChanged.connect(self.print_item_clicked)


        # Displays button to open selected directory in the file browser
        self.show_folder_button = QPushButton()
        self.show_folder_button.setText("Open selected folder in File Browser")
        self.show_folder_button.clicked.connect(self.open_folder)
        self.show_folder_button.show()

        # ________________________LAYOUTS+WIDGETS________________________

        # Put the find folder button and folder selected button together
        layer_one.addWidget(self.select_a_folder_button)
        layer_one.addWidget(self.directory_label)

        # Image paths of selected folder
        layer_two.addWidget(self.file_paths_list_widget)

        layer_three.addLayout(layer_three_vertical_one)

        layer_three_vertical_two.addWidget(self.show_folder_button)
        layer_three.addLayout(layer_three_vertical_two)

        # Put the "convert to png" button beneath
        vertical_layout_parent.addLayout(layer_one)
        vertical_layout_parent.addLayout(layer_two)
        vertical_layout_parent.addLayout(layer_three)

        widget.setLayout(vertical_layout_parent)
        self.setCentralWidget(widget)

    # Gets the selected item from the list of files in the selected folder
    # Called when user clicks
    def print_item_clicked(self):
        # Dereferences the QListWidget object and gets the value of the 'text' field
        print(self.file_paths_list_widget.currentItem().text())

    # Prompts user to select a folder, stores the given folder path and displays chosen path to user
    def select_folder_prompt(self):
        #  Clear self.file_list and QListWidget to prepare for newly selected folder.
        self.file_list.clear()
        self.file_paths_list_widget.clear()

        # Append a "/" otherwise it will mix the folder name and containing image file together
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory")) + "/"
        # Update QLabel to new directory, and store it in self for future use
        self.directory_label.setText(directory)
        self.directory_path_name = directory

        # Update self.file_list field
        file_list = self.scan_for_jpg_file_paths()
        self.file_list = file_list

        # Populated the QListWindow() with the update self.file_list field
        self.file_paths_list_widget.addItems(self.file_list)

    # Given a path name, will open it in the Folder browser app
    def open_folder(self):
        subprocess.call(["open", "-R", self.directory_path_name])

    # Given the current state of the directory_path_name folder, will scan for image files in that folder
    def scan_for_jpg_file_paths(self):
        file_list = []

        for root, dirs, files in os.walk(self.directory_path_name, topdown=True):
            for filename in files:
                if '.jpeg' or '.jpg' or '.webp' or '.gif' or '.icns' in filename:
                    if '.png' not in filename:
                        absolute_path = self.directory_path_name + filename
                        # Avoid adding duplicates
                        if absolute_path not in file_list:
                            file_list.append(absolute_path)

        return file_list


app = QApplication(sys.argv)
w = MainWindow()
w.show()

app.exec()
