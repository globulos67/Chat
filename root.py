# --- Librairy --- #

# Root Lib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QVBoxLayout, QScrollArea, QPushButton, QLineEdit, QWidget, QGridLayout
from PyQt5.QtCore import QSize

# Root Edit Lib
import win32con
import win32gui
import win32api

# Thread Lib
import threading

# --- Created Scripts --- #

# Login Script
import Login.Login

# Client Script
import client

# Time
import time

# JSON Lib
import json

# Ctype
import ctypes

#---------------------Color Value----------------------#
theme = {}

# Opening JSON file
theme_file = open("SecureChat v.1.1.0/theme.json")

# returns JSON object as 
# a dictionary
theme_data = json.load(theme_file)

for value in theme_data['Theme']:
    theme[value["Name"]] = {"text_color": value["Text Color"], "border_color": value["Border Color"], "background_color": value["Background Color"], "window_color": value["Window Color"]}
  
# Closing file
theme_file.close()

#---------------------Root[Class Object]----------------------#
class Root(QMainWindow):
    def __init__(self, name: str = "Root", size=[800, 600], fullscreen=False):
        super(Root, self).__init__()
        self.name = name
        self.size = QSize(size[0], size[1])
        self.set_name("Welcome", self)
        self.resize(self.size)
        self.username = ""
        self.lock = threading.Lock()
        self.current_theme = theme["Blue Eyes"]
        print(f"Current Theme: {self.current_theme}")

        # Central widget
        self.central_widget = QFrame(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Login Entry
        self.login_entry = QLineEdit(self.central_widget)
        self.login_entry.returnPressed.connect(self.on_loginned)
        self.layout.addWidget(self.login_entry)

        self.create()

    #---------------------Login----------------------#

    def on_loginned(self):
        self.username = self.login_entry.text()
        self.user = client.Client(self.username)
        self.close()

        self.loginned_window = QMainWindow()
        self.root_id = self.winId()

        self.set_size(self.size, self.loginned_window)
        self.set_name(f"{self.name}: {self.username}", self.loginned_window)
        self.set_title_bar_color(self.loginned_window, self.current_theme["window_color"])

        self.userframe = {}
        self.user_inconv = ""

        self.current_frame = None

        # Menu Frame
        self.create_menu()

        # Chat Frame
        self.chat_frame = QFrame()
        self.chat_frame.setAutoFillBackground(True)
        self.chat_frame.setStyleSheet(f"background-color: {self.current_theme['background_color']}; border: 1px solid {self.current_theme['border_color']};")

        # Create a QGridLayout
        self.grid_layout = QGridLayout()
        # Add the frame to the layout
        self.grid_layout.addWidget(self.chat_frame, 0, 0)

        # Set the stretch factor of the row containing the frame
        self.grid_layout.setRowStretch(0, 1)

        # Create a central widget and set the layout on it
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.grid_layout)

        # Set the central widget of the main window
        self.loginned_window.setCentralWidget(self.central_widget)
    

        # Créer une barre de défilement verticale
        self.message_scrollarea = QScrollArea(self.chat_frame)
        self.message_scrollarea.setWidgetResizable(True)
        self.chat_frame.layout = QVBoxLayout(self.chat_frame)
        self.chat_frame.layout.addWidget(self.message_scrollarea)

        # Créer un widget pour contenir les messages
        self.messages_widget = QWidget()
       
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_widget.setLayout(self.messages_layout)

        # Ajouter le widget des messages à la zone de défilement
        self.message_scrollarea.setWidget(self.messages_widget)

        # Bouton pour envoyer un message
        self.send_button = QPushButton("Send", self.chat_frame)
        self.send_button.setStyleSheet(f"background-color: {self.current_theme['background_color']}; border: 1px solid {self.current_theme['border_color']}; color: {self.current_theme['text_color']};")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Afficher la fenêtre de chat
        self.loginned_window.show()

        # Démarrer le thread de réception de messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    #---------------------Menu----------------------#

    def create_menu(self):
        menu_bar = self.loginned_window.menuBar()
        theme_menu = menu_bar.addMenu("Theme")

        for theme_name in theme:
            theme_action = QtWidgets.QAction(theme_name, self.loginned_window)
            theme_action.triggered.connect(lambda checked, name=theme_name: self.change_theme(name))
            theme_menu.addAction(theme_action)

    def change_theme(self, theme_name):
        self.current_theme = theme[theme_name]
        self.loginned_window.setStyleSheet(f"background-color: {self.current_theme['window_color']};")
        self.chat_frame.setStyleSheet(f"background-color: {self.current_theme['background_color']}; border: 1px solid {self.current_theme['border_color']};")
        self.send_button.setStyleSheet(f"background-color: {self.current_theme['background_color']}; border: 1px solid {self.current_theme['border_color']}; color: {self.current_theme['text_color']};")

    #---------------------Chat----------------------#

    def send_message(self):
        message = self.message_entry.text()
        if message:
            self.user.send_message(message)
            self.message_entry.clear()

    def receive_messages(self):
        while True:
            time.sleep(0.1)
            messages = self.user.receive_message()
            if messages:
                for message in messages:
                    self.display_message(message)

    def display_message(self, message):
        message_label = QLabel(message, self.messages_widget)
        message_label.setStyleSheet(f"color: {self.current_theme['text_color']};")
        self.messages_layout.addWidget(message_label)

    #---------------------Util----------------------#

    def set_size(self, size, window):
        window.resize(size.width(), size.height())

    def set_name(self, name, window):
        window.setWindowTitle(name)

    def set_title_bar_color(self, window, color):
    # Set the title bar color using a hexadecimal value
        window.setStyleSheet(f"background-color: {color};")  # Set color to red

    
