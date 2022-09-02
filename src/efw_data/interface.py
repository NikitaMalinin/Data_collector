import sys
import csv
import pandas as pd

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextBrowser, \
    QPushButton, QLabel, QMessageBox, QComboBox, QCheckBox, QFileDialog, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from commands import dict_result_dfs, get_basis, get_fatigue_stress, get_adjustment_factors, get_maintenance_tasks

path_FatigueKomplett = ''
path_FR_STR = ''
path_PAX_to_GMF = ''


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Main window parameters
        self.resize(1024, 768)  # Measures
        self.setWindowTitle("EFW Data (demo version)")  # Program title

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        menu = self.menuBar()
        menu_help = menu.addMenu("&Help")

        menu_help_about = QAction('&About', self)
        menu_help.addAction(menu_help_about)
        menu_help_about.triggered.connect(self.show_about_window)

    def show_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.show()


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setWindowTitle("About")  # Program title

        self.labelText = QLabel(
            'EFW Data (demo version)'
            + 2*'\n' + 'Program was created to collect input data for fatigue calculations'
            + 2*'\n' + 'Program output:'
            + '\n' + '- Stress basis' + '\n' + '- Fatigue stress'
            + '\n' + '- Adjustment factors' + '\n' + '- Maintenance tasks'
            + 2*'\n' + 'Author: Nikita Malinin'
            + '\n' + 'E-mail: nikita.malinin175@gmail.com'
        )

        self.labelText.adjustSize()
        # self.setFixedSize(self.labelText.size())
        self.layoutMain = QHBoxLayout()
        self.layoutMain.addWidget(self.labelText, 0, Qt.AlignTop)

        self.setLayout(self.layoutMain)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()  # Super class calling

        # Message boxes
        self.msgBoxInfo = QMessageBox()
        self.msgBoxInfo.setIcon(QMessageBox.Information)

        self.msgBoxCritical = QMessageBox()
        self.msgBoxCritical.setIcon(QMessageBox.Critical)

        try:
            df_positions = pd.read_csv(path_FR_STR)
            self.list_stringer = df_positions['Stringer'].dropna().values.astype(str).tolist()
            self.list_frame = df_positions['Frame'].values.astype(str).tolist()

            self.dict_PAX_to_GMF = {}
            for row in csv.reader(open(path_PAX_to_GMF)):
                self.dict_PAX_to_GMF[row[0]] = row[1]

        except Exception as e:
            self.list_stringer = []
            self.list_frame = []
            print(e.__class__)
            self.msgBoxCritical.setWindowTitle("Error")
            self.msgBoxCritical.setText(str(e.__class__))
            self.msgBoxCritical.exec()

        # Solving of problem with table alignment after tabulating
        fixed_font = QFont("monospace")
        fixed_font.setStyleHint(QFont.TypeWriter)

        # Text Browser
        self.textStatus = QTextBrowser()
        self.textStatus.setMaximumWidth(168)
        self.textStatus.setLineWrapMode(False)
        self.textStatus.append("Press Start")

        self.textResults = QTextBrowser()
        self.textResults.setLineWrapMode(False)
        self.textResults.setFont(fixed_font)
        self.textResults.setMinimumWidth(400)

        # Labels
        self.labelFrames = QLabel('Frame range:')
        self.labelStringers = QLabel('Stringer range:')
        self.labelSide = QLabel('Side:')
        self.labelElements = QLabel('Considered elements:')
        self.labelOutput = QLabel('Output data:')

        # Combo Boxes
        self.comboBoxFrameFWD = QComboBox()
        self.comboBoxFrameFWD.addItems(self.list_frame[18:])
        self.comboBoxFrameFWD.setMinimumWidth(65)

        self.comboBoxFrameAFT = QComboBox()
        self.comboBoxFrameAFT.addItems(self.list_frame[18:])
        self.comboBoxFrameAFT.setMinimumWidth(65)

        self.comboBoxStringerUP = QComboBox()
        self.comboBoxStringerUP.addItems(self.list_stringer)
        self.comboBoxStringerUP.setMinimumWidth(65)

        self.comboBoxStringerLOW = QComboBox()
        self.comboBoxStringerLOW.addItems(self.list_stringer)
        self.comboBoxStringerLOW.setMinimumWidth(65)

        self.comboBoxSide = QComboBox()
        self.comboBoxSide.addItems(['LH', 'RH'])
        self.comboBoxSide.setMinimumWidth(65)

        # PushButtons
        self.pushButtonStart = QPushButton("Start", self)
        self.pushButtonStart.resize(self.pushButtonStart.sizeHint())
        self.pushButtonStart.clicked.connect(self.on_pushButtonStart_clicked)

        self.pushButtonExport = QPushButton("Export", self)
        self.pushButtonExport.resize(self.pushButtonExport.sizeHint())
        self.pushButtonExport.clicked.connect(self.on_pushButtonExport_clicked)

        # Check Boxes
        self.checkBoxFrame = QCheckBox("Frame", self)
        self.checkBoxFrame.setChecked(True)
        self.checkBoxStringer = QCheckBox("Stringer", self)
        self.checkBoxStringer.setChecked(True)
        self.checkBoxSkin = QCheckBox("Skin", self)
        self.checkBoxSkin.setChecked(True)
        self.checkBoxStress = QCheckBox("Fatigue stress", self)
        self.checkBoxStress.setChecked(True)
        self.checkBoxAF = QCheckBox("Adjustment factors", self)
        self.checkBoxAF.setChecked(True)
        self.checkBoxTasks = QCheckBox("Maintenance tasks", self)
        self.checkBoxTasks.setChecked(True)

        # Layouts
        self.layoutMain = QHBoxLayout()
        self.layoutRightPanel = QVBoxLayout()
        self.layoutLeftPanel = QVBoxLayout()
        self.layoutSetParams = QVBoxLayout()
        self.layoutElements = QHBoxLayout()
        self.layoutStressBasis = QVBoxLayout()
        self.layoutStatus = QVBoxLayout()
        self.layoutResults = QVBoxLayout()

        self.layoutButtons = QHBoxLayout()

        self.layoutFrameRange = QHBoxLayout()
        self.layoutStringerRange = QHBoxLayout()

        # Group Boxes
        self.grBoxParams = QGroupBox("Parameters")
        # self.grBoxParams.setCheckable(True)
        self.grBoxStatus = QGroupBox("Status")
        self.grBoxResults = QGroupBox("Results")

        # Add objects in layouts
        self.layoutFrameRange.addWidget(self.comboBoxFrameFWD, 0, Qt.AlignLeft)
        self.layoutFrameRange.addWidget(self.comboBoxFrameAFT, 1, Qt.AlignLeft)
        self.layoutStringerRange.addWidget(self.comboBoxStringerUP, 0, Qt.AlignLeft)
        self.layoutStringerRange.addWidget(self.comboBoxStringerLOW, 1, Qt.AlignLeft)
        self.layoutElements.addWidget(self.checkBoxFrame, 0, Qt.AlignLeft)
        self.layoutElements.addWidget(self.checkBoxStringer, 0, Qt.AlignLeft)
        self.layoutElements.addWidget(self.checkBoxSkin, 1, Qt.AlignLeft)

        self.layoutButtons.addWidget(self.pushButtonStart, 0, Qt.AlignCenter)
        self.layoutButtons.addWidget(self.pushButtonExport, 0, Qt.AlignCenter)

        self.layoutSetParams.addWidget(self.labelFrames)
        self.layoutSetParams.addLayout(self.layoutFrameRange)
        self.layoutSetParams.addWidget(self.labelStringers)
        self.layoutSetParams.addLayout(self.layoutStringerRange)
        self.layoutSetParams.addWidget(self.labelSide)
        self.layoutSetParams.addWidget(self.comboBoxSide, 0, Qt.AlignLeft)
        self.layoutSetParams.addWidget(self.labelElements)
        self.layoutSetParams.addLayout(self.layoutElements)
        self.layoutSetParams.addWidget(self.labelOutput)
        self.layoutSetParams.addWidget(self.checkBoxStress, 0, Qt.AlignLeft)
        self.layoutSetParams.addWidget(self.checkBoxAF, 0, Qt.AlignLeft)
        self.layoutSetParams.addWidget(self.checkBoxTasks, 0, Qt.AlignLeft)

        self.grBoxParams.setLayout(self.layoutSetParams)

        self.layoutStatus.addWidget(self.textStatus, 0, Qt.AlignLeft)
        self.grBoxStatus.setLayout(self.layoutStatus)

        self.layoutLeftPanel.addWidget(self.grBoxParams, 0, Qt.AlignLeft)
        self.layoutLeftPanel.addLayout(self.layoutButtons)
        self.layoutLeftPanel.addWidget(self.grBoxStatus, 0, Qt.AlignLeft)

        # Right Panel
        self.layoutResults.addWidget(self.textResults)
        self.grBoxResults.setLayout(self.layoutResults)
        self.layoutRightPanel.addWidget(self.grBoxResults)
        self.layoutMain.addLayout(self.layoutLeftPanel)
        self.layoutMain.addLayout(self.layoutRightPanel)

        self.setLayout(self.layoutMain)

    def on_pushButtonStart_clicked(self):
        try:
            self.textResults.clear()
            self.textResults.append('Reference file - ' + str(path_FatigueKomplett))

            self.dict_element_status = {
                'Frame': [self.checkBoxFrame.isChecked(), '300-FR', 'frame'],
                'Stringer': [self.checkBoxStringer.isChecked(), '300-STR', 'stringer'],
                'Skin': [self.checkBoxSkin.isChecked(), '300-SKIN', 'skin']
            }

            self.side = self.comboBoxSide.currentText()

            get_basis()

            if self.checkBoxStress.isChecked():
                get_fatigue_stress()

            if self.checkBoxAF.isChecked():
                get_adjustment_factors()

            if self.checkBoxTasks.isChecked():
                get_maintenance_tasks()

            self.textStatus.clear()
            self.textStatus.append("Search in progress..." + "\n" + "Done!")
            self.msgBoxInfo.setText('Search is done!')
            self.msgBoxInfo.exec()

        except Exception as e:
            print(e.__class__)
            self.msgBoxCritical.setWindowTitle("Error")
            self.msgBoxCritical.setText(str(e.__class__))
            self.msgBoxCritical.exec()

    def on_pushButtonExport_clicked(self):
        try:
            text = self.textResults.toPlainText()

            if text == '':
                self.msgBoxInfo.setText('Text browser is empty')
                self.msgBoxInfo.exec()
                return

            text_split = []
            text_row = []
            for i in text.split('\n'):
                for j in i.split('|'):
                    text_row.append(j)
                text_split.append(text_row)
                text_row = []

            file_name, file_format = QFileDialog \
                .getSaveFileName(self, 'Save file', '', 'Excel Workbook (*.xlsx);;CSV (Comma delimited) (*.csv)')
            if file_name == '':
                return

            if file_format == 'Excel Workbook (*.xlsx)':
                sheet_output = 'EFW_Data_Output'
                row_number = 1
                # TODO: DataFrame.to_excel() does not work correctly when .xlsx file and internal sheet are already created
                df_empty = pd.DataFrame()
                # with pd.ExcelWriter(file_name, mode='w', engine='openpyxl') as writer_xlsx:
                #     worksheet = writer_xlsx.book.create_sheet(title=sheet_output)
                with pd.ExcelWriter(file_name, mode='w', engine='openpyxl') as writer_xlsx:
                    df_empty.to_excel(writer_xlsx, sheet_name=sheet_output,
                                      index=False)  # Temporary solution of issue above
                    for element in dict_result_dfs.keys():
                        for parameter in dict_result_dfs[element].keys():
                            if dict_result_dfs[element][parameter] is not None:
                                writer_xlsx.sheets[sheet_output].cell(row_number, 1).value = element + ' ' + parameter
                                dict_result_dfs[element][parameter] \
                                    .to_excel(writer_xlsx, sheet_name=sheet_output, startrow=row_number)
                                row_number += dict_result_dfs[element][parameter].shape[0] + 3
                        row_number += 1
                    if self.checkBoxTasks.isChecked():
                        self.df_maintenance_tasks_result \
                            .to_excel(writer_xlsx, sheet_name=sheet_output, startrow=row_number, index=False)

            if file_format == 'CSV (Comma delimited) (*.csv)':
                with open(file_name, 'w', newline='') as csv_file:
                    writer_csv = csv.writer(csv_file, delimiter=',')
                    writer_csv.writerows(text_split)

            self.msgBoxInfo.setText('Export is done!')
            self.msgBoxInfo.exec()

        except Exception as e:
            print(e.__class__)
            self.msgBoxCritical.setWindowTitle("Error")
            self.msgBoxCritical.setText(str(e.__class__))
            self.msgBoxCritical.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())