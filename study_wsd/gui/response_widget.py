from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPlainTextEdit

from study_wsd.db import WsdResult

class ResponseWidget(QWidget):
    def __init__(self, result:WsdResult):
        super().__init__()
        self.result = result
        self.initUI()

    def initUI(self):
        # Create widgets
        lbl_response = QLabel()
        log = QPlainTextEdit()
        import json
        log.setPlainText(json.dumps(self.result.log[1]["content"]))
        

        lbl_response.setText(self.result.answer_response)
        color = "green" if self.result.correct else "red"
        self.setStyleSheet("QWidget {\nbackground-color: " + color + ";}")
        lbl_response.setText(" " + self.result.model_id + " answered " + self.result.answer_response + ", the correct answer was " + self.result.answer_value)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(lbl_response)
        layout.addWidget(log)

        # Set widget layout
        self.setLayout(layout)
