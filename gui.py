from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
import sys
import main_app


class CertificateToolGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Define fetch_button as an attribute
        self.fetch_button = None
        self.result = None

        self.init_ui()

    def init_ui(self):
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)  # Make it read-only

        # update_button = QPushButton('Update Certificates')
        check_button = QPushButton('Check Certificates')
        self.fetch_button = QPushButton('Update Missing Certificates')

        # update_button.clicked.connect(lambda: self.run_action(main_app.update_certificates_gui))
        check_button.clicked.connect(lambda: self.run_action(main_app.check_certificates_gui))
        self.fetch_button.clicked.connect(lambda: self.run_action_fetch(main_app.fetch_certificates_gui))
        self.fetch_button.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.log_text)
        # layout.addWidget(update_button)
        layout.addWidget(check_button)
        layout.addWidget(self.fetch_button)

        self.setLayout(layout)

    def run_action(self, action_function):
        self.log_text.clear()  # Clear existing logs
        # Check if the action_function is main_app.check_certificates_gui
        if action_function == main_app.check_certificates_gui:
            # Call the function and store its return value
            self.result = main_app.check_certificates_gui(self.append_log)
            if self.result:
                self.fetch_button.setVisible(True)
        else:
            # For other functions, simply call them without storing the return value
            action_function(self.append_log)

    def run_action_fetch(self, action_function):
        self.log_text.clear()
        action_function(self.append_log, self.result)

    def append_log(self, log_message):
        self.log_text.append(log_message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CertificateToolGUI()
    window.show()
    sys.exit(app.exec_())
