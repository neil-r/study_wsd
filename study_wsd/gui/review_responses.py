import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QWidget,QPlainTextEdit, QHBoxLayout, QScrollArea, QLabel, QPushButton
from study_wsd.gui import response_widget
from study_wsd import db
from study_wsd import wse
from study_wsd import wse_prompts


class MyDialog(QDialog):
    def __init__(self, database:db.DatabaseSqlLite):
        super().__init__()
        self.database = database
        self.evaluation_offset_value = 1

        self.initUI()

    def initUI(self):

        # GUI Widget Tree
        ## self Base Widget (Hortionzal Layout)
        ### Control Widget (Vertical Layout)
        #### Toolbar Widget (Horiontal layout)
        #### Model List Widget (multi-selection box)
        ### Data Widget (Vertical Layout)
        #### Evaluation Navigation (Horitonal Layout)
        ##### Back (button)
        ##### Evaluation (textbox)
        ##### Next (button)
        #### Response Viewer (Scrollable Vertical Layout)
        ##### List of response Widgets

        # Create layout and add widgets
        layout = QHBoxLayout()
        control_widget = QWidget()
        data_widget = QWidget()

        layout.addWidget(control_widget)
        layout.addWidget(data_widget)

        # Set dialog layout
        self.setLayout(layout)

        # Set Control Widget
        layout_cw = QVBoxLayout()

        #TODO implement controls gui

        control_widget.setLayout(layout_cw)

        # Set Data Widget
        
        layout_dw = QVBoxLayout()

        evaluation_navigation_widget = QWidget()
        layout_enw = QHBoxLayout()

        self.btn_next = QPushButton(">")
        self.btn_next.clicked.connect(self.next_button_clicked)
        self.btn_previous = QPushButton("<")
        self.btn_previous.clicked.connect(self.previous_button_clicked)
        self.txt_evaluation = QPlainTextEdit()

        self.txt_evaluation.setMinimumHeight(200)
        self.txt_evaluation.setMinimumWidth(300)
        layout_enw.addWidget(self.btn_previous)
        layout_enw.addWidget(self.txt_evaluation)
        layout_enw.addWidget(self.btn_next)

        evaluation_navigation_widget.setLayout(layout_enw)

        responses_scroll_widget = QScrollArea(control_widget)

        self.response_list_widget = QWidget()
        self.response_list_layout = QVBoxLayout()
        self.response_list_layout.addWidget(QLabel("Hello"))
        self.response_list_widget.setLayout(self.response_list_layout)
        responses_scroll_widget.setWidget(self.response_list_widget)
        responses_scroll_widget.setWidgetResizable(True)

        layout_dw.addWidget(evaluation_navigation_widget)
        layout_dw.addWidget(responses_scroll_widget)

        data_widget.setLayout(layout_dw)

        # Set dialog properties
        self.setWindowTitle('Word Sense Disambiguation Evaluation Reviewer')
        self.setGeometry(300, 300, 300, 150)

    def reset_data(self):
        # self.btn_previous.setEnabled(self.evaluation_offset_value > 1)
            
        results = self.database.get_wsd_evaluation(self.evaluation_offset_value)
        count = self.response_list_layout.count()
        while count > 0:
            item = self.response_list_layout.itemAt(0)
            self.response_list_layout.removeItem(item)
            count = self.response_list_layout.count()
            item.widget().deleteLater()

        if len(results) > 0:
            r1 = results[0]
            wse_obj = wse.WordSenseEvaluation.From_json(r1.evalution)
            p = wse_prompts.DefaultWsePrompt(wse_obj)
            self.txt_evaluation.setPlainText(p.content)
            i = 0
            for r in results:
                print(str(r))
                w = response_widget.ResponseWidget(r)
                self.response_list_layout.insertWidget(i, w)
                i += 1

    def next_button_clicked(self):
        print("next clicked")
        self.evaluation_offset_value += 1
        self.reset_data()
    
    def previous_button_clicked(self):
        print("previous clicked")
        self.evaluation_offset_value -= 1
        self.reset_data()

    def onOKButtonClick(self):
        print('OK Button Clicked')
        self.accept()  # Close the dialog

    def onCancelButtonClick(self):
        print('Cancel Button Clicked')
        self.reject()  # Close the dialog

if __name__ == '__main__':
  app = QApplication(sys.argv)

  dialog = MyDialog(db.DatabaseSqlLite())
  result = dialog.exec_()  # Show the dialog and get the result
