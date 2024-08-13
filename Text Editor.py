import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QInputDialog, QMessageBox, QColorDialog, QStyleFactory
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor
from PyQt5.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)
        
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 12))
        self.setCentralWidget(self.text_edit)
        
        self.create_menus()
        self.file_path = None
        
        self.dark_mode = False
        self.set_dark_mode(True)

    def create_menus(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.create_action("New", self.new_file))
        file_menu.addAction(self.create_action("Open", self.open_file))
        file_menu.addAction(self.create_action("Save", self.save_file))
        file_menu.addAction(self.create_action("Save As", self.save_file_as))
        file_menu.addSeparator()
        file_menu.addAction(self.create_action("Exit", self.close))

        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction(self.create_action("Undo", self.undo))
        edit_menu.addAction(self.create_action("Redo", self.redo))
        edit_menu.addSeparator()
        edit_menu.addAction(self.create_action("Cut", self.cut))
        edit_menu.addAction(self.create_action("Copy", self.copy))
        edit_menu.addAction(self.create_action("Paste", self.paste))

        # Format Menu
        format_menu = menubar.addMenu("Format")
        format_menu.addAction(self.create_action("Bold", self.toggle_bold))
        format_menu.addAction(self.create_action("Italic", self.toggle_italic))
        format_menu.addAction(self.create_action("Underline", self.toggle_underline))
        format_menu.addSeparator()
        format_menu.addAction(self.create_action("Change Font Size", self.change_font_size))
        format_menu.addAction(self.create_action("Text Color", self.change_text_color))

        # View Menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction(self.create_action("Toggle Dark Mode", self.toggle_dark_mode))

        # About Menu
        about_menu = menubar.addMenu("About")
        about_menu.addAction(self.create_action("About Editor", self.show_about_info))

        # Help Menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction(self.create_action("Contents", self.show_help_contents))

    def create_action(self, text, slot):
        action = QAction(text, self)
        action.triggered.connect(slot)
        return action

    def new_file(self):
        self.text_edit.clear()
        self.file_path = None

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text files (*.txt);;All files (*)")
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_edit.setText(content)
            self.file_path = file_path

    def save_file(self):
        if not self.file_path:
            self.save_file_as()
        else:
            with open(self.file_path, "w") as file:
                file.write(self.text_edit.toPlainText())

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text files (*.txt);;All files (*)")
        if file_path:
            self.file_path = file_path
            self.save_file()

    def undo(self):
        self.text_edit.undo()

    def redo(self):
        self.text_edit.redo()

    def cut(self):
        self.text_edit.cut()

    def copy(self):
        self.text_edit.copy()

    def paste(self):
        self.text_edit.paste()

    def toggle_bold(self):
        cursor = self.text_edit.textCursor()
        format = QTextCharFormat()
        format.setFontWeight(QFont.Bold if cursor.charFormat().fontWeight() == QFont.Normal else QFont.Normal)
        cursor.mergeCharFormat(format)

    def toggle_italic(self):
        cursor = self.text_edit.textCursor()
        format = QTextCharFormat()
        format.setFontItalic(not cursor.charFormat().fontItalic())
        cursor.mergeCharFormat(format)

    def toggle_underline(self):
        cursor = self.text_edit.textCursor()
        format = QTextCharFormat()
        format.setFontUnderline(not cursor.charFormat().fontUnderline())
        cursor.mergeCharFormat(format)

    def change_font_size(self):
        size, ok = QInputDialog.getInt(self, "Change Font Size", "Enter new font size:", min=1)
        if ok:
            cursor = self.text_edit.textCursor()
            format = QTextCharFormat()
            format.setFontPointSize(size)
            cursor.mergeCharFormat(format)

    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cursor = self.text_edit.textCursor()
            format = QTextCharFormat()
            format.setForeground(QColor(color.name()))
            cursor.mergeCharFormat(format)

    def show_about_info(self):
        QMessageBox.information(self, "About", "Simple Text Editor\n\nVersion 1.0\n\nDeveloped By Sahampath")

    def show_help_contents(self):
        QMessageBox.information(self, "Help", "This is a simple text editor.\nYou can open, edit, and save text files.")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.set_dark_mode(self.dark_mode)

    def set_dark_mode(self, enabled):
        dark_style = """
            QMainWindow, QMenuBar, QMenu, QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background-color: #3a3a3a;
            }
            QMenu::item {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #444444;
            }
        """
        light_style = """
            QMainWindow, QMenuBar, QMenu, QTextEdit {
                background-color: #ffffff;
                color: #000000;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background-color: #e0e0e0;
            }
            QMenu::item {
                background-color: #ffffff;
                color: #000000;
            }
            QTextEdit {
                border: 1px solid #cccccc;
            }
        """
        self.setStyleSheet(dark_style if enabled else light_style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion")) 
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
