import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow, QMessageBox, QPushButton, QGridLayout, QLineEdit, QFormLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIntValidator
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
        'ico': 'Bitmap Icon file',
        'tiff': 'Tagged Image File Format',
        'webp': 'WebP image file',
    },
    'video': {
        'mp4': 'MPEG-4 video file',
        'mov': 'Apple QuickTime movie file',
        'mkv': 'Matroska Multimedia Container',
        'avi': 'Audio Video Interleave',
        'wmv': 'Windows Media Video',
        'webm': 'WebM video file',
    },
    'document': {
        'pdf': 'Portable Document Format',
    }
}
def getFileCategory(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return None

class ConverterWindow(QMainWindow):
    def __init__(self, file_path, newext, options=None) -> None:
        super().__init__()
        self.setWindowTitle('ConvertLite')
        self.setFixedSize(400, 200)
        self.file_path = file_path
        self.newext = newext
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.options = options if options is not None else {}
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.label = QLabel(f"Converting {self.file_path} to {self.newext}", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.show()
        self.convertFile()



    def convertFile(self):
        _, ext = os.path.splitext(self.file_path)
        ext = ext.lstrip('.').lower()  # Remove the dot and lowercase
        file_category = getFileCategory(ext)

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

        reply = QMessageBox.question(self, 'Finished!',
                                 "Do you want to convert another file?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.openDropWindow()
        else:
            self.close()
            exit(0)



    def openDropWindow(self):
        self.close()
    
        self.dropWindow = DropWindow() 
        self.dropWindow.show()

    def convertImage(self):
        try:
            with Image.open(self.file_path) as img:
                if self.options:  # Check if there are any options
                    img = img.resize((int(self.options.get('width')), int(self.options.get('height'))))
                target_file = self.file_path.rsplit('.', 1)[0] + '.' + self.newext
                img.save(target_file)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to convert image: {e}")
            exit(1)

    def convertVideo(self):
        try:
            # Load the video file
            clip = VideoFileClip(self.file_path)
            if self.options:  # Beispiel für Video
                clip = clip.resize(newsize=(int(clip.w), int(clip.h)), width=int(self.options.get('width')), height=int(self.options.get('height')))
                clip = clip.set_fps(int(self.options.get('fps')))

            # Define the target file name with the new extension
            target_file = self.file_path.rsplit('.', 1)[0] + '.' + self.newext
            
            # Depending on the extension, you might need different methods or settings
            # For simplicity, we're using write_videofile which should work for common formats
            clip.write_videofile(target_file)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to convert video: {e}")
            exit(1)


class CustomButton(QPushButton):
    clickedWithShift = pyqtSignal()
    def __init__(self, text, parent=None, tag=None):
            super().__init__(text, parent)
            self.tag = tag  # Speichere das tag für späteren Gebrauch

    def mousePressEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            self.clickedWithShift.emit()
        else:
            super().mousePressEvent(event)

class GridListWindow(QMainWindow):
    def __init__(self, elements, file_path):
        super().__init__()
        self.setWindowTitle('ConvertLite')
        self.setFixedSize(300, 400)
        self.file_path = file_path
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        # create label for info
        

        # Use CustomButton for clickable elements
        for tag, primary_text, secondary_text in elements:
            button = CustomButton(f"{primary_text}\n{secondary_text}", self, tag=tag)
            button.clicked.connect(lambda checked, tag=tag: self.element_clicked(tag))
            button.clickedWithShift.connect(lambda tag=tag: self.handleShiftClick(tag))




            layout.addWidget(button)

        hint_label = QLabel("Hold shift while choosing format to configure properties")
        hint_label.setFont(QFont("Arial", 8))  
        hint_label.setStyleSheet("color: gray;")  
        hint_label.setAlignment(Qt.AlignCenter)  
        layout.addWidget(hint_label)  
        self.show()

    def handleShiftClick(self, tag):
        config_win = ConfigurationWin(tag, self.file_path, self.openConversionWindow)
        config_win.show()
        self.current_config_win = config_win




    def element_clicked(self, tag):
        self.openConversionWindow(tag)


    def openEmptyWindow(self, newext):
        self.new_window = ConverterWindow(self.file_path, newext)
        self.new_window.show()

    def config_window(self, tag):
        # Pass a method as the convert_callback to ConfigurationWin
        config_win = ConfigurationWin(tag, self.file_path, self.convert_callback)
        config_win.show()

    def convert_callback(self, file_path, newext, options):
        self.openConversionWindow(newext, options)

    def openConversionWindow(self, newext, options=None):  # options hinzugefügt
        self.new_window = ConverterWindow(self.file_path, newext, options)
        self.new_window.show()


class ConfigurationWin(QMainWindow):
    def __init__(self, tag, file_path, openConversionWindow):
        super().__init__()
        self.setWindowTitle(f'Configuration for {tag}')
        self.setFixedSize(400, 300)
        
        self.file_path = file_path
        self.tag = tag
        
        self.openConversionWindow = openConversionWindow

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        file_type = getFileCategory(self.tag)
        
        self.intValidator = QIntValidator(1, 99999)

        self.config_form = QFormLayout()

        if file_type == 'image':
            self.imageWidthInput = QLineEdit()
            self.imageWidthInput.setValidator(self.intValidator)  # Validator setzen
            self.config_form.addRow("Width (px):", self.imageWidthInput)
            
            self.imageHeightInput = QLineEdit()
            self.imageHeightInput.setValidator(self.intValidator)  # Validator setzen
            self.config_form.addRow("Height (px):", self.imageHeightInput)
        elif file_type == 'video':
            self.videoFpsInput = QLineEdit()
            self.videoFpsInput.setValidator(self.intValidator)  # Validator setzen für FPS, angenommen FPS ist auch eine ganze Zahl
            self.config_form.addRow("FPS:", self.videoFpsInput)
        
        layout.addLayout(self.config_form)
        
        goButton = QPushButton("Go", self)
        goButton.clicked.connect(self.startConversion)
        layout.addWidget(goButton)

        self.show()

    # Start the conversion with the specified configurations
    def startConversion(self):
        options = {}
        if getFileCategory(self.tag) == 'image':
            options['width'] = self.imageWidthInput.text()
            options['height'] = self.imageHeightInput.text()
        elif getFileCategory(self.tag) == 'video':
            options['fps'] = self.videoFpsInput.text()
        
        # Rufen Sie hier direkt openConversionWindow auf
        self.openConversionWindow(self.tag, options)
        self.close()






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
