from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class GradesWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

    def file_select(self):
        selected_file = QFileDialog.getOpenFileName(self, "Select Data File")

        with open(selected_file, "r") as f:
            next(f)
            for line in f:
                parts = line.split(",")
                self.student_ids.append(int(parts[0]))
                self.original_grades.append(int(parts[1]))
                self.corrected_grades = self.original_grades



    


if __name__ == '__main__':
    app = QApplication()
    window = QMainWindow()
    window.show()
    app.exec()