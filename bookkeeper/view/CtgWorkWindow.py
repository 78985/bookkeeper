"""Всё, что касается окна редактирования категорий и его функционала"""
from PyQt6 import QtWidgets, QtGui


class CategoryAUDWindow(QtWidgets.QWidget):
    """# Создадим окно редактирования категории"""

    def __init__(self,
                 ctg_adder=None,
                 ctg_updater=None,
                 ctg_deleter=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Выполнен вход в окно редактирования категорий')
        self.ctg_adder = ctg_adder
        self.ctg_updater = ctg_updater
        self.ctg_deleter = ctg_deleter

        self.ButtonLabel = self.MakeLabel('Выбери один из вариантов')

        self.CtgAddCheck = self.MakeButton('Создать категорию')
        self.CtgUpdCheck = self.MakeButton('Обновить категорию')
        self.CtgDelCheck = self.MakeButton('Удалить категорию')

        self.CtgName = self.MakeLineEdit(
            'Введи имя категории БЕЗ ПРОБЕЛОВ. Чувствителен к регистру.')
        self.CtgParent = self.MakeLineEdit(
            'Введи имя родителя БЕЗ ПРОБЕЛОВ. Чувствителен к регистру.')
        self.CtgChildrens = self.MakeLineEdit(
            'Введи имена детей через пробелы. (На свой страх и риск)')

        self.AcceptButton = self.MakeButton('Подтвердить')

        vert = QtWidgets.QVBoxLayout()

        vert.addWidget(self.ButtonLabel)

        horiz = QtWidgets.QHBoxLayout()
        horiz.addWidget(self.CtgAddCheck)
        horiz.addWidget(self.CtgUpdCheck)
        horiz.addWidget(self.CtgDelCheck)

        vert.addLayout(horiz)

        vert.addWidget(self.CtgName)
        vert.addWidget(self.CtgParent)
        vert.addWidget(self.CtgChildrens)

        vert.addWidget(self.AcceptButton)

        self.setLayout(vert)

        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.clicked.connect(self.ctg_add1)
        self.CtgUpdCheck.clicked.connect(self.ctg_upd1)
        self.CtgDelCheck.clicked.connect(self.ctg_del1)

        print('Окно сформировано')
    def ctg_add1(self) -> None:
        """# Добавление часть 1"""
        print('Вошли в режим добавления')

        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_add2)
    def ctg_add2(self) -> None:
        """# Добавление часть 2"""
        self.AcceptButton.clicked.disconnect(self.ctg_add2)
        print('Начат второй этап добавления')
        print(f'{self.CtgName.text()}, '
              f'{self.CtgParent.text()}, '
              f'{self.CtgChildrens.text()}')
        self.ctg_adder(self.CtgName.text(),
                       self.CtgParent.text(),
                       self.CtgChildrens.text())
        print('Добавление в БД выполнено')
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Добавление завершено. Сброс до исходного состояния произведён.')
    def ctg_upd1(self) -> None:
        """# обновление часть 1"""
        print('Вошли в режим обновления')
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_upd2)

    def ctg_upd2(self) -> None:
        """# обновление часть 2"""
        self.AcceptButton.clicked.disconnect(self.ctg_upd2)
        print('Начат второй этап обновления')
        print(f'{self.CtgName.text()}, '
              f'{self.CtgParent.text()}, '
              f'{self.CtgChildrens.text()}')
        self.ctg_updater(self.CtgName.text(),
                         self.CtgParent.text(),
                         self.CtgChildrens.text())
        print('Обновление в БД выполнено')
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Обновление завершено. Сброс до исходного состояния произведён.')
    def ctg_del1(self) -> None:
        """# Удаление часть 1"""
        print('Вошли в режим удаления')
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_del2)
    def ctg_del2(self) -> None:
        """# Удаление часть 2"""
        self.AcceptButton.clicked.disconnect(self.ctg_del2)
        print('Начат второй этап удаления')
        print(f'{self.CtgName.text()}')
        self.ctg_deleter(self.CtgName.text())
        print('Удаление в БД выполнено')
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Удаление завершено. Сброс до исходного состояния произведён.')
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
        """# Функция создания кнопки"""
        Button_obj = QtWidgets.QPushButton(text)
        return Button_obj
