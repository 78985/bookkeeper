""" Полное описание основного рабочего окна"""
import os
from PyQt6 import QtWidgets, QtGui
from bookkeeper.view.ExpensesTable import ExpenseTable
from bookkeeper.view.BudgetTable import BudgetTable
from bookkeeper.view.DeleteLine import DeleteLine
from bookkeeper.view.ExpAddCompany import ExpAddCompany
from bookkeeper.models.category import Category

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Start_pic_path = os.path.join(BASE_DIR, 'StartPic.jpg')


class BookkeeperWindow(QtWidgets.QWidget):
    """ Класс основного рабочего окна"""

    def __init__(self,
                 ctg: list[Category] = [Category('Empty')],
                 expenses_adder=None,
                 expenses_updater=None,
                 expenses_deleter=None,
                 ctg_pk_2_name=None,
                 category_adder=None,
                 category_updater=None,
                 category_deleter=None,
                 budget_updater=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TableLabel = self.MakeLabel('Таблица последних расходов')

        self.DeleteLine = DeleteLine(expenses_deleter)
        self.DeleteLine.setMaximumWidth(300)
        self.ExpensesTable = ExpenseTable(expenses_updater, ctg_pk_2_name)

        self.BudgetLabel = self.MakeLabel('Бюджет')

        self.BudgetTable = BudgetTable(budget_updater)

        self.ExpenseAndCategoryEdit = ExpAddCompany(ctg,
                                                    expenses_adder,
                                                    category_adder,
                                                    category_updater,
                                                    category_deleter)

        horiz0 = QtWidgets.QHBoxLayout()
        horiz0.addWidget(self.TableLabel)
        horiz0.addWidget(self.DeleteLine)
        vert1 = QtWidgets.QVBoxLayout()
        vert1.addLayout(horiz0)
        vert1.addWidget(self.ExpensesTable)
        vert1.addWidget(self.BudgetLabel)
        vert1.addWidget(self.BudgetTable)
        vert1.addWidget(self.ExpenseAndCategoryEdit)

        self.layout = vert1
        self.setLayout(self.layout)

    def MakeLabel(self, text: str = 'empty label') -> QtWidgets.QLabel:
        """# Функция создания подписи у чего-либо"""
        label_obj = QtWidgets.QLabel()
        label_obj.setText(text)
        return label_obj

    def MakeLineEdit(self, text: str = '') -> QtWidgets.QLineEdit:
        """# Функция создания поля с возможностью ввода"""

        LineEdit_obj = QtWidgets.QLineEdit()
        LineEdit_obj.setPlaceholderText(text)
        return LineEdit_obj

    def MakeButton(self, text: str = 'empty button') -> QtWidgets.QPushButton:
        """ # Функция создания кнопки"""
        Button_obj = QtWidgets.QPushButton(text)
        return Button_obj
