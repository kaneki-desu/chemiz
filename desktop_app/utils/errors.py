from PyQt5.QtWidgets import QMessageBox

def show_error(window, message):
    QMessageBox.critical(window, "Error", message)

def show_warning(window, message):
    QMessageBox.warning(window, "Warning", message)

def show_info(window, message):
    QMessageBox.information(window, "Success", message)
