import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow, QMessageBox, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
import os
import time
from scripts.FileHelper import get_file_name_without_extension, get_full_file_name, get_file_type
from PIL import Image
from moviepy.editor import VideoFileClip

FILE_CATEGORIES = {
    'image': {
        'png': 'Portable Network Graphics',
        'jpg': 'JPEG image',
        'jpeg': 'JPEG image',
        'gif': 'Graphics Interchange Format',
        'bmp': 'Bitmap image file',
        'svg': 'Scalable Vector Graphics',
    },
    'video': {
        'mp4': 'MPEG-4 video file',
        'mov': 'Apple QuickTime movie file',
        'mkv': 'Matroska Multimedia Container',
    },
    'document': {
        'pdf': 'Portable Document Format',
    }
}

class ConverterWindow(QMainWindow):
    def __init__(self, file_path, newext) -> None:
        super().__init__()
        self.setWindowTitle('ConvertLite')
        self.setFixedSize(400, 200)
        self.file_path = file_path
        self.newext = newext
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.label = QLabel(f"Converting {self.file_path} to {self.newext}", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.show()
        self.convertFile()

    def getFileCategory(self, extension):
            for category, extensions in FILE_CATEGORIES.items():
                if extension in extensions:
                    return category
            return None

    def convertFile(self):
        _, ext = os.path.splitext(self.file_path)
        ext = ext.lstrip('.').lower()  # Remove the dot and lowercase
        file_category = self.getFileCategory(ext)

        if file_category == 'image':
            self.convertImage()
        elif file_category == 'video':
            self.convertVideo()
            pass
        elif file_category == 'document':
            # Placeholder for document conversion logic
            pass
        else:
            QMessageBox.warning(self, "Error", "Unsupported file format.")
            exit(1)

    def convertImage(self):
        try:
            with Image.open(self.file_path) as img:
                target_file = self.file_path.rsplit('.', 1)[0] + '.' + self.newext
                img.save(target_file)
                exit(0)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to convert image: {e}")
            exit(1)

    def convertVideo(self):
        try:
            # Load the video file
            clip = VideoFileClip(self.file_path)
            
            # Define the target file name with the new extension
            target_file = self.file_path.rsplit('.', 1)[0] + '.' + self.newext
            
            # Depending on the extension, you might need different methods or settings
            # For simplicity, we're using write_videofile which should work for common formats
            clip.write_videofile(target_file)
            
            QMessageBox.information(self, "Success", f"Video converted successfully to {self.newext}!")
            exit(0)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to convert video: {e}")
            exit(1)
class GridListWindow(QMainWindow):
    def __init__(self, elements, file_path):
        super().__init__()
        self.setWindowTitle('File Options')
        self.setFixedSize(400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.file_path = file_path
         # Use QPushButton for clickable elements
        for tag, primary_text, secondary_text in elements:
            button = QPushButton(f"{primary_text}\n{secondary_text}", self)
            button.clicked.connect(lambda checked, tag=tag: self.element_clicked(tag))
            layout.addWidget(button)

        self.show()

    def add_element_to_grid(self, tag, primary_text, secondary_text):
        button = QPushButton(f"{primary_text}\n{secondary_text}")
        button.clicked.connect(lambda: self.element_clicked(tag))
        position = len(self.grid_layout.children())  # Current number of widgets in grid
        row = position // 3  # Adjust the divisor based on your desired grid width
        column = position % 3
        self.grid_layout.addWidget(button, row, column)

    def element_clicked(self, tag):
        self.openEmptyWindow(tag)
        self.hide()

    def openEmptyWindow(self, newext):
        # Pass the data to GridListWindow
        self.new_window = ConverterWindow(self.file_path, newext)
        self.new_window.show()
    



class DropWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ConvertLite')
        self.setFixedSize(400, 200)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Drop a File here", self)
        self.label.setToolTip("Drag and drop a file here")
        self.label.setToolTipDuration(2000)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        self.file_name = None
        self.file_name_without_extension = None
        self.file_type = None
        self.file_path = None

        self.elementsList = None
        # Enable dragging and dropping onto the GUI
        self.setAcceptDrops(True)
    def getFileCategory(self, file_extension):
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                return category
        return None

    def generateElementsExcludingCurrentType(self, file_type):
        category = self.getFileCategory(file_type)
        if not category:
            raise NotImplementedError(f"File type {file_type} is not supported, supported types are: {', '.join(FILE_CATEGORIES.keys())}")
        elements = []
        for ext, description in FILE_CATEGORIES[category].items():
            if ext != file_type:  # Correctly exclude the current file type
                element_tag = str(ext)
                element_primary_text = f"{ext.upper()} file"
                element_secondary_text = description
                elements.append((element_tag, element_primary_text, element_secondary_text))
        return elements

    def showError(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(message)
        msgBox.setWindowTitle("ConvertLite")
        msgBox.exec_()



    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            if files:
                # Just take the first file for simplicity
                file_path = files[0]
                self.label.setText(f"Found: {file_path}")
            else:
                self.label.setText("Drop a File here")
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            # Just take the first file for simplicity
            file_path = files[0]
            self.processFile(file_path)
            self.openEmptyWindow()
            self.hide()

    def processFile(self, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            if not os.path.isfile(file_path):
                raise Exception(f"Invalid file: {file_path}")
            

            # Let the processing begin
            # First we get the filename, filename without extension and file type
            self.file_name = get_full_file_name(file_path)
            self.file_name_without_extension = get_file_name_without_extension(file_path)
            self.file_type = get_file_type(file_path).lower()
            self.file_path = file_path

            self.elementsList = self.generateElementsExcludingCurrentType(self.file_type)
            # Now lets wait for the user to decide what to do with the file
            return # Show next window - Processing complete
        except Exception as e:
            self.showError(str(e))
            exit(1)
        


    def openEmptyWindow(self):
        # Pass the data to GridListWindow
        self.new_window = GridListWindow(self.elementsList, self.file_path)
        self.new_window.show()



def main():
    app = QApplication(sys.argv)
    window = DropWindow()
    window.show()
    sys.exit(app.exec_())

main()
