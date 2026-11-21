import sys
import os
import subprocess
from About import AboutWindow
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class GradesWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.setWindowTitle("Grades Manager")
        self.setMinimumSize(640, 600)

        # Load stylesheet
        qss_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        with open(qss_path, "r") as f:
            self.setStyleSheet(f.read())

        self._build_ui()

    # ------------------------------------------------------------------ #
    #  UI construction                                                     #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # --- top bar ---
        top_bar = QHBoxLayout()
        self.lbl_file = QLabel("No file selected")
        self.lbl_file.setObjectName("lblFile")
        self.btn_open = QPushButton("📂  Open Student File")
        self.btn_open.setObjectName("btnOpen")
        self.btn_open.clicked.connect(self.file_select)
        self.btn_update = QPushButton("💾  Update File")
        self.btn_update.setObjectName("btnUpdate")
        self.btn_update.clicked.connect(self.update_file)
        self.btn_about = QPushButton("ℹ️  About")
        self.btn_about.setObjectName("btnAbout")
        self.btn_about.clicked.connect(self.open_about)
        top_bar.addWidget(self.lbl_file, stretch=1)
        top_bar.addWidget(self.btn_open)
        top_bar.addWidget(self.btn_update)
        top_bar.addWidget(self.btn_about)
        root.addLayout(top_bar)

        # --- bonus bar ---
        bonus_bar = QHBoxLayout()
        lbl_bonus = QLabel("Grade Bonus:")
        lbl_bonus.setObjectName("lblBonus")
        self.spin_bonus = QSpinBox()
        self.spin_bonus.setObjectName("spinBonus")
        self.spin_bonus.setRange(-100, 100)
        self.spin_bonus.setValue(0)
        self.spin_bonus.setFixedWidth(90)
        self.spin_bonus.setAlignment(Qt.AlignCenter)
        self.spin_bonus.editingFinished.connect(self.correct_grades)   # fires on Enter
        bonus_bar.addWidget(lbl_bonus)
        bonus_bar.addWidget(self.spin_bonus)
        bonus_bar.addStretch()
        root.addLayout(bonus_bar)

        # --- table ---
        self.table = QTableWidget(50, 3)
        self.table.setObjectName("gradesTable")
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        root.addWidget(self.table, stretch=1)


    def file_select(self):
        selected_file, _ = QFileDialog.getOpenFileName(
            self, "Select Student Data File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not selected_file:
            return  # user cancelled

        self.selected_file = selected_file
        self.lbl_file.setText(os.path.basename(selected_file))

        self.student_ids.clear()
        self.original_grades.clear()
        self.corrected_grades.clear()

        with open(selected_file, "r") as f:
            next(f)
            for line in f:
                parts = line.split(",")
                self.student_ids.append(int(parts[0]))
                self.original_grades.append(int(parts[1]))

        self.corrected_grades = list(self.original_grades)

        self.update_table()

    # ------------------------------------------------------------------ #
    #  Table update                                                        #
    # ------------------------------------------------------------------ #
    def update_table(self):
        """Populate the table from student_ids, original_grades, corrected_grades."""
        self.table.clearContents()

        for row, (sid, orig, corr) in enumerate(
            zip(self.student_ids, self.original_grades, self.corrected_grades)
        ):
            id_item   = QTableWidgetItem(str(sid))
            orig_item = QTableWidgetItem(str(orig))
            corr_item = QTableWidgetItem(str(corr))

            for item in (id_item, orig_item, corr_item):
                item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, orig_item)
            self.table.setItem(row, 2, corr_item)

    def correct_grades(self):
        correction_value = self.spin_bonus.value()
        for i in range(len(self.original_grades)):
            if self.original_grades[i] + correction_value > 100: self.corrected_grades[i] = 100
            elif self.original_grades[i] + correction_value < 0: self.corrected_grades[i] = 0
            else:
                self.corrected_grades[i] = self.original_grades[i] + correction_value
        self.update_table()

    def update_file(self):
        with open(self.selected_file, 'w') as f:
            f.write('ID,Grade\n')
            for i in range(len(self.corrected_grades)):
                f.write(f'{self.student_ids[i]},{self.corrected_grades[i]}\n')


        # Open in the default spreadsheet app (cross-platform)
        if sys.platform == "win32":
            os.startfile(self.selected_file)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Microsoft Excel", self.selected_file])
        else:
            subprocess.Popen(["xdg-open", self.selected_file])

    def open_about(self):
        self._about_window = AboutWindow()
        self._about_window.show()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GradesWindow()
    window.show()
    sys.exit(app.exec())