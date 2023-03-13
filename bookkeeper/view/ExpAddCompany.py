"""# Группа виджетов, в которой можно добавлять расходы и вызвать
окно редактирования категорий"""
from PyQt6 import QtWidgets
from bookkeeper.models.category import Category
from bookkeeper.view.EasyComboBox import EasyComboBox
from bookkeeper.view.CtgWorkWindow import CategoryAUDWindow


class ExpAddCompany(QtWidgets.QGroupBox):
    """# Группа виджетов, в которой можно добавлять расходы и вызвать
    окно редактирования категорий"""

    def __init__(self,
                 ctg: list[Category] | None = None,
                 expense_adder=None,
                 ctg_adder=None,
                 ctg_updater=None,
                 ctg_deleter=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expense_adder = expense_adder
        self.ctg_adder = ctg_adder
        self.ctg_updater = ctg_updater
        self.ctg_deleter = ctg_deleter
        self.ExpenseLabel = self.MakeLabel('Сумма')
        self.ExpenseField = self.MakeLineEdit('Введи сумму')

        self.CategoryLabel = self.MakeLabel('Категория')
        self.CategoryLabel.setMaximumWidth(60)
        self.CategoryBox = EasyComboBox()
        self.CategoryBox.setMaximumWidth(1200)
        self.CategoryEditButton = self.MakeButton('Редактировать категории')
        self.CategoryEditButton.setMaximumWidth(200)

        self.CommLabel = self.MakeLabel('Комментарий')
        self.CommField = self.MakeLineEdit('Введи комментарий (опционально)')

        self.ExpenseAccept = self.MakeButton('Добавить расход')

        horiz1 = QtWidgets.QHBoxLayout()
        horiz1.addWidget(self.ExpenseLabel)
        horiz1.addWidget(self.ExpenseField)

        vert1 = QtWidgets.QVBoxLayout()
        vert1.addLayout(horiz1)

        horiz2 = QtWidgets.QHBoxLayout()
        horiz2.addWidget(self.CategoryLabel)
        horiz2.addWidget(self.CategoryBox)
        horiz2.addWidget(self.CategoryEditButton)

        vert1.addLayout(horiz2)

        horiz3 = QtWidgets.QHBoxLayout()
        horiz3.addWidget(self.CommLabel)
        horiz3.addWidget(self.CommField)

        vert1.addLayout(horiz3)

        vert1.addWidget(self.ExpenseAccept)

        self.setLayout(vert1)

        self.ExpenseAccept.clicked.connect(self.add_expense)
        self.CategoryEditButton.clicked.connect(self.ctg_edit_show_window)

        self.set_categories(ctg)
    def set_categories(self, ctg: list[Category] | None) -> None:
        """
            # Установка категорий: их добавление в выпадающее меню
        Parameters
        ----------
        ctg

        Returns
        -------

        """
        self.categories = ctg
        if ctg is None:
            self.CategoryBox.set_items(['Empty'])
        else:
            self.ctg_names = [category.name for category in ctg]
            print(f'Получены имена {self.ctg_names}')
            self.CategoryBox.set_items(self.ctg_names)
    def add_expense(self) -> None:
        """# Опишем процедуру добавления расхода"""
        print('Приняты данные на добавление')
        amount = self.ExpenseField.text()
        print('Считано число')
        category = self.CategoryBox.currentText()
        print('Считана категория')
        comm = self.CommField.text()
        print('Считан комментарий')
        print('Передаём данные в сощдатель')
        self.expense_adder(amount, category, comm)
        self.ExpenseField.clear()
        self.CategoryBox.clear()
        self.CommField.clear()
    def ctg_edit_show_window(self) -> None:
        """Редактор вида окна"""
        self.window2 = CategoryAUDWindow(self.ctg_adder,
                                         self.ctg_updater,
                                         self.ctg_deleter)
        self.window2.setWindowTitle('Изменение Категорий')
        self.window2.resize(300, 600)
        self.window2.show()

    def MakeLabel(self, text: str = 'empty label') -> QtWidgets.QLabel:
        """  # Функция создания подписи у чего-либо"""
        label_obj = QtWidgets.QLabel()
        label_obj.setText(text)
        return label_obj

    def MakeLineEdit(self, text: str = '') -> QtWidgets.QLineEdit:
        """ # Функция создания поля с возможностью ввода"""
        LineEdit_obj = QtWidgets.QLineEdit()
        LineEdit_obj.setPlaceholderText(text)
        return LineEdit_obj

    def MakeButton(self, text: str = 'empty button') -> QtWidgets.QPushButton:
        """# Функция создания кнопки"""
        Button_obj = QtWidgets.QPushButton(text)
        return Button_obj
