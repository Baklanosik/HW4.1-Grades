from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPixmap

class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('About Me')
        self.setStyleSheet("font-size: 30; font-weight: bold")

        self.my_name = QLabel("Feliks Kagan", self)
        self.my_name.setGeometry(40,20,80,30)
        self.email = QLabel("kagan.f47@gmail.com", self)
        self.email.setGeometry(130,20,150,30)

        image = QPixmap('Afeka.png').scaled(269,110)

        self.my_picture = QLabel(self)
        self.my_picture.setGeometry(20,70,269,110)
        self.my_picture.setPixmap(image)

        linkedin_label = QLabel('<a href="https://www.linkedin.com/in/felix-kagan-a26aab3a2/">My Linkedin', self)
        linkedin_label.setOpenExternalLinks(True)
        linkedin_label.setGeometry(120,200,100,30)
        github_label = QLabel('<a href="https://github.com/Baklanosik/HW4.1-Grades">GitHub Repository', self)
        github_label.setOpenExternalLinks(True)
        github_label.setGeometry(100,230,200,30)

if __name__ == '__main__':
    app = QApplication()
    window = AboutWindow()
    window.show()
    app.exec()