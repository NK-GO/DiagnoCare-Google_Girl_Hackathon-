from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar, QAction, QStatusBar, QMessageBox, QInputDialog, QMainWindow, QScrollArea
from src.bot import Query, Reply

class MyHealthCareBot(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()
		self.query = Query()

	def initUI(self):
		self.setWindowTitle('AI-Powered HealthCare Chatbot')
		self.setGeometry(100, 100, 600, 400)
		
		self.label = QLabel('Enter patient description:')
		self.submit_button = QPushButton('Submit')
		self.output_label = QLabel()
		self.output_label.setWordWrap(True)
		self.input_text = QLineEdit()
		self.label.setStyleSheet('''
		    QLabel {
		        font-size: 18px; /* set font size for label */
		        color: #AAAAAA; /* set text color */
		    }
		''')
		
		self.input_text.setStyleSheet('''
		    QLineEdit {
		        padding: 10px; /* set padding for input text */
		        border: 2px solid #007BFF; /* set border color */
		    }
		''')
		self.submit_button.setStyleSheet('''
		    QPushButton {
		        padding: 10px; /* set padding for button */
		        background-color: #007BFF; /* set background color */
		        color: #ffffff; /* set text color */
		        border: none; /* remove border */
		    }
		
		    QPushButton:hover {
		        background-color: #0056b3; /* set background color on hover */
		    }
		''')		
		menu_bar = self.menuBar()
		options_menu = menu_bar.addMenu('Options')
		history_menu = menu_bar.addMenu('History')

		set_age_action = QAction('Set Age', self)
		set_age_action.triggered.connect(self.show_set_age_dialog)
		options_menu.addAction(set_age_action)

		set_gender_action = QAction('Set Gender', self)
		set_gender_action.triggered.connect(self.show_set_gender_dialog)
		options_menu.addAction(set_gender_action)

		show_history_action = QAction('Show Chat History', self)
		show_history_action.triggered.connect(self.show_history)
		history_menu.addAction(show_history_action)

		remove_history_action = QAction('Remove Chat History', self)
		remove_history_action.triggered.connect(self.remove_history)
		history_menu.addAction(remove_history_action)

		self.status_bar = QStatusBar()
		self.setStatusBar(self.status_bar)

		layout = QVBoxLayout()
		layout.addWidget(self.label)
		layout.addWidget(self.input_text)
		layout.addWidget(self.submit_button)
		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)
		scroll_area.setWidget(self.output_label)
		layout.addWidget(scroll_area)

		central_widget = QWidget()
		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)

		self.setLayout(layout)
		
		self.submit_button.clicked.connect(self.process_input)

	def show_set_age_dialog(self):
		age, ok = QInputDialog.getInt(self, 'Set Age', 'Enter age:', 0, 0, 150)
		if ok:
			self.query.set_param("age", str(age))
			self.status_bar.showMessage('Age set to: {}'.format(age))

	def show_set_gender_dialog(self):
		gender, ok = QInputDialog.getText(self, 'Set Gender', 'Enter gender (e.g. male, female):')
		if ok:
			self.query.set_param("gender", gender)
			self.status_bar.showMessage('Gender set to: {}'.format(gender))

	def show_history(self):
		self.output_label.setText("test")
		# TODO
		# self.output_label.setText(Reply(self.query).retrive_history())
	
	def remove_history(self):
		self.output_label.setText("")
		# TODO
		# self.output_label.setText(Reply(self.query).delete_history())

	def process_input(self):
		user_input = self.input_text.text()

		self.query.set_message(user_input)

		bot_output = Reply(self.query.create_message()).send(True)

		self.output_label.setText(bot_output)
