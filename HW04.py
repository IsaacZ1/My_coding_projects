import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QListView, QAbstractItemView, QMessageBox, QLineEdit)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

class Calculator(QWidget):

    def __init__(self):
        super(Calculator, self).__init__()
        self.setWindowTitle("ISyE 2027 Calculator")

        self.list_view = QListView()
        self.list_model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.list_model)

        self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)

        self.line_edit1 = QLineEdit()
        self.line_edit2 = QLineEdit()

        self.line_edit1.textChanged.connect(self.enable_buttons)
        self.line_edit2.textChanged.connect(self.enable_buttons)

        self.addition_button = QPushButton("+")
        self.addition_button.setEnabled(False)
        self.addition_button.clicked.connect(self.add_operator)

        self.subtract_button = QPushButton("-")
        self.subtract_button.setEnabled(False)
        self.subtract_button.clicked.connect(self.subtract_operator)

        self.multiplication_button = QPushButton("*")
        self.multiplication_button.setEnabled(False)
        self.multiplication_button.clicked.connect(self.multiply_operator)

        self.division_button = QPushButton("/")
        self.division_button.setEnabled(False)
        self.division_button.clicked.connect(self.divide_operator)

        vbox = QVBoxLayout()
        vbox.addWidget(self.list_view)
        vbox.addWidget(self.line_edit1)
        vbox.addWidget(self.line_edit2)
        vbox.addWidget(self.addition_button)
        vbox.addWidget(self.subtract_button)
        vbox.addWidget(self.multiplication_button)
        vbox.addWidget(self.division_button)
        self.setLayout(vbox)

    def add_operator(self):
    	number1 = float(self.line_edit1.text())
    	number2 = float(self.line_edit2.text())
    	sum1 = number1 + number2
    	sum1 = round(sum1,4)
    	equation = QStandardItem("{} + {} =".format(self.line_edit1.text(),self.line_edit2.text()))
    	self.list_model.appendRow(equation)
    	answer = QStandardItem("          " + str(sum1))
    	self.list_model.appendRow(answer)
    	self.list_view.setModel(self.list_model)
    	self.line_edit1.setText('')
    	self.line_edit1.setFocus()
    	self.line_edit2.setText('')
    	self.line_edit2.setFocus()

    def subtract_operator(self):
    	number1 = float(self.line_edit1.text())
    	number2 = float(self.line_edit2.text())
    	difference1 = number1 - number2
    	difference1 = round(difference1,4)
    	equation = QStandardItem("{} - {} =".format(self.line_edit1.text(),self.line_edit2.text()))
    	self.list_model.appendRow(equation)
    	answer = QStandardItem("          " + str(difference1))
    	self.list_model.appendRow(answer)
    	self.list_view.setModel(self.list_model)
    	self.line_edit1.setText('')
    	self.line_edit1.setFocus()
    	self.line_edit2.setText('')
    	self.line_edit2.setFocus()
    def multiply_operator(self):
    	number1 = float(self.line_edit1.text())
    	number2 = float(self.line_edit2.text())
    	product1 = number1 * number2
    	product1 = round(product1,4)
    	equation = QStandardItem("{} * {} =".format(self.line_edit1.text(),self.line_edit2.text()))
    	self.list_model.appendRow(equation)
    	answer = QStandardItem("          " + str(product1))
    	self.list_model.appendRow(answer)
    	self.list_view.setModel(self.list_model)
    	self.line_edit1.setText('')
    	self.line_edit1.setFocus()
    	self.line_edit2.setText('')
    	self.line_edit2.setFocus()
    def divide_operator(self):
	   	if int(self.line_edit2.text()) == 0:
	   		QMessageBox.about(self,"Divide by 0 error","Dividing by zero does not exist")	
	   		self.line_edit1.setText('')
	   		self.line_edit1.setFocus()
	   		self.line_edit2.setText('')
	   		self.line_edit2.setFocus()
	   	else:
	   		number1 = float(self.line_edit1.text())
	   		number2 = float(self.line_edit2.text())
	   		quotient1 = number1 / number2
	   		quotient1 = round(quotient1,4)
	   		equation = QStandardItem("{} / {} =".format(self.line_edit1.text(),self.line_edit2.text()))
	   		self.list_model.appendRow(equation)
	   		answer = QStandardItem("          " + str(quotient1))
	   		self.list_model.appendRow(answer)
	   		self.list_view.setModel(self.list_model)
	   		self.line_edit1.setText('')
	   		self.line_edit1.setFocus()
	   		self.line_edit2.setText('')
	   		self.line_edit2.setFocus()
    def enable_buttons(self):
        if len(self.line_edit1.text()) == 0 or len(self.line_edit2.text()) == 0:
            self.addition_button.setEnabled(False)
            self.subtract_button.setEnabled(False)
            self.multiplication_button.setEnabled(False)
            self.division_button.setEnabled(False)
        else:
            self.addition_button.setEnabled(True)
            self.subtract_button.setEnabled(True)
            self.multiplication_button.setEnabled(True)
            self.division_button.setEnabled(True)


if __name__=='__main__':
    app = QApplication(sys.argv)
    main = Calculator()
    main.show()
    exit_code = app.exec_()
    sys.exit(exit_code)