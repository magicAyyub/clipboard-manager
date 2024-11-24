import os
import sys
import re
import pyperclip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QListWidget, QLineEdit, QPushButton, QListWidgetItem,
                             QCheckBox, QLabel, QGraphicsOpacityEffect)
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize

# Suppress IMKClient messages
os.environ['PYQT_MAC_USE_COCOA'] = '1'

class Toast(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        # Create main layout
        layout = QVBoxLayout(self)
        
        # Create inner widget for background color
        self.inner = QWidget()
        self.inner.setStyleSheet("""
            background-color: rgba(52, 53, 65, 0.95);
            border-radius: 8px;
            padding: 2px;
        """)
        
        # Create label for text
        self.label = QLabel(text)
        self.label.setStyleSheet("""
            color: white;
            padding: 8px;
            font-size: 14px;
            font-weight: 500;
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        
        # Add label to inner widget
        inner_layout = QVBoxLayout(self.inner)
        inner_layout.addWidget(self.label)
        inner_layout.setContentsMargins(4, 4, 4, 4)
        
        # Add inner widget to main layout
        layout.addWidget(self.inner)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Set window flags and attributes
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # Setup opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

    def show_toast(self):
        self.opacity_effect.setOpacity(0)
        self.show()
        
        # Fade in animation
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_in_animation.start()
        
        # Schedule fade out
        QTimer.singleShot(2000, self.start_fade_out)

    def start_fade_out(self):
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out_animation.finished.connect(self.hide)
        self.fade_out_animation.start()

class ClipboardTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard Tracker")
        self.setGeometry(100, 100, 400, 600)
        self.clipboard_history = []
        self.initUI()
        
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(500)
        
        self.last_clipboard_content = pyperclip.paste()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)  # Add spacing between elements
        
        # Search bar with icon
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search clipboard history...")
        self.search_bar.textChanged.connect(self.filter_history)
        self.search_button = QPushButton()  # Changed to self.search_button for styling
        self.search_button.setObjectName("searchButton")  # Set a unique object name
        self.search_button.setIcon(QIcon.fromTheme("edit-find"))
        self.search_button.setFixedSize(QSize(70, 35))  # Smaller size
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout, stretch=0)
        
        # Checkbox with espace between text
        self.remove_formatting_checkbox = QCheckBox(" Remove formatting on copy")    
        layout.addWidget(self.remove_formatting_checkbox)
        
        # List widget
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.copy_item)
        layout.addWidget(self.history_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Add spacing between buttons
        
        # Copy button
        self.copy_button = QPushButton(" Copy")
        self.copy_button.setIcon(QIcon.fromTheme("edit-copy"))
        self.copy_button.clicked.connect(self.copy_selected)
        button_layout.addWidget(self.copy_button)
        
        # Clear button
        self.clear_button = QPushButton(" Clear History")
        self.clear_button.setIcon(QIcon.fromTheme("edit-clear"))
        self.clear_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        self.apply_styles()

    def show_toast(self, message):
        toast = Toast(message, self)
        if len(message.split()) >= 3:
            toast.setFixedWidth(300)
        else:
            toast.setFixedWidth(150)
        toast.setFixedHeight(60)
        x = 10  # Offset from left
        y = 10  # Offset from top
        toast.move(x, y)
        toast.show_toast()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton QIcon {
                margin-right: 8px;  /* Add spacing between icon and text */
            }
            QPushButton#searchButton {  /* Specific style for search button */
                background-color: #4CAF50;  
                color: white;
                font-size: 12px;
                border-radius: 8px;
                min-width: 60px;  /* Smaller width */
                padding: 5px;  /* Reduce padding */
            }
            QPushButton#searchButton:hover {  /* Hover effect */
                background-color: #45a049;
            }
            QCheckBox {
                font-size: 14px;
                margin: 8px 0;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #e0e0e0;
                background-color: white;
                border-radius: 4px;
            }
        """)

    def on_clipboard_change(self):
        content = self.clipboard.text()
        if content:
            if self.remove_formatting_checkbox.isChecked():
                content = self.remove_formatting(content)
                pyperclip.copy(content)  # Copy cleaned content back to clipboard
                self.show_toast("Formatted text removed and copied.")
            else:
                self.show_toast("Text copied.")
            self.clipboard_history.insert(0, content)
            self.update_history_list()

    def check_clipboard(self):
        current_content = pyperclip.paste()
        if current_content != self.last_clipboard_content:
            self.last_clipboard_content = current_content
            self.on_clipboard_change()

    def update_history_list(self):
        self.history_list.clear()
        for item in self.clipboard_history:
            list_item = QListWidgetItem(item[:50] + "..." if len(item) > 50 else item)
            list_item.setToolTip(item)
            self.history_list.addItem(list_item)

    def filter_history(self, text):
        for i in range(self.history_list.count()):
            item = self.history_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def copy_selected(self):
        if self.history_list.currentItem():
            content = self.history_list.currentItem().toolTip()
            pyperclip.copy(content)
            self.show_toast(f"Text added to history.")

    def copy_item(self, item):
        content = item.toolTip()
        pyperclip.copy(content)
        self.show_toast(f"Text copied.")

    def clear_history(self):
        self.clipboard_history.clear()
        self.update_history_list()
        self.show_toast("Clipboard history cleared")

    def remove_formatting(self, text):
        # Remove extra whitespace and line breaks
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tracker = ClipboardTracker()
    tracker.show()
    sys.exit(app.exec())