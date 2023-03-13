"""
Кусок таблицы, отвечающей за вывод бюджета и
работу пользователя с ним
"""
from typing import Any
from PyQt6 import QtWidgets
from bookkeeper.models.budget import Budget


class BudgetTable(QtWidgets.QTableWidget):
    """
    # Создаём класс таблицы.
    # Он отличается тем, что все данные о настройке
    # таблицы вытащим в отдельное
    # место, а потом воткнём в приложение.
    # Также тут собрана вся логика работы с данными в табличке,
    # которые потом отправляются на обработку в БД и далее
    """

    def __init__(self,
                 budget_modifier=None,
                 rws: int = 3,
                 clmns: int = 4,
                 header_text: str = 'Срок Сумма Бюджет Ключ',
                 *args, **kwargs) -> None:
        super().__init__(*args, *kwargs)
        self.budget_modifier = budget_modifier
        self.setColumnCount(clmns)
        self.setRowCount(rws)
        self.setHorizontalHeaderLabels(header_text.split())
        for j in range(clmns):
            self.resizeColumnToContents(j)
        self.SetTableData([['День', 'empty', 'empty'],
                           ['Неделя', 'empty', 'empty'],
                           ['Месяц', 'empty', 'empty']])

        self.budget_attrs = {0: 'День', 1: 'Неделя', 2: 'Месяц'}

        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)

        self.cellDoubleClicked.connect(self.cell_double_clicked)

    def SetTableData(self, data: list[list[Any]] | None = None) -> None:
        """
        # Функция заполнения полей таблицы
        """
        if data is None:
            data = [['empty' for j in range(self.columnCount())]
                    for j in range(self.rowCount())]
        self.data = data

        for j, row in enumerate(data):
            for k, x in enumerate(row):
                self.setItem(j, k, QtWidgets.QTableWidgetItem(x))
        for j in range(self.columnCount()):
            self.resizeColumnToContents(j)
    def cell_double_clicked(self, row: int, columns: int) -> None:
        """
        # Обработка события двойного щелчка - ожидаем обработки редактирования
        """
        print('Начали ожидать конца редактирования')
        self.cellChanged.connect(self.cell_changed)
    def cell_changed(self, row, column) -> None:
        """
        # Обрабатывается окончание редактирования -
        # составляем новые параметры записи
        """
        print('Приступили к обработке события после конца редактирования')
        self.cellChanged.disconnect(self.cell_changed)
        pk = self.data[row][-1]
        print('Определили ключ записи')
        new_val = self.item(row, column).text()
        print('Определили новые параметры бюджета')
        attr = self.budget_attrs[row]
        print('Вернули имя атрибута, которому меняли значение')
        print(f'Передаём на вход: {pk}, {new_val}, {attr}')
        self.budget_modifier(pk, new_val, attr)

    def set_budgets(self, budgets: list[Budget]) -> None:
        """ # Запись в таблицу бюджета из БД """
        self.budgets = budgets
        self.data = self.budgets_to_data(self.budgets)
        self.clearContents()
        self.SetTableData(self.data)

    def budgets_to_data(self, budgets: list[Budget]) -> list[list[str]]:
        """
        # Конвертер из типов характерных для Budget
        # в строки
        Parameters
        ----------
        budgets

        Returns
        -------

        """
        data = []
        if budgets is None:
            data = [['День', '', 'Не определён', ''],
                    ['Неделя', '', 'Не определён', ''],
                    ['Месяц', '', 'Не определён', '']]
        else:
            for time in ['День', 'Неделя', 'Месяц']:
                budget = [bdg for bdg in budgets if bdg.time == time]
                if len(budget) == 0:
                    data.append([time, '', 'Не определён', ''])
                else:
                    bdg = budget[0]
                    data.append([str(bdg.time),
                                 str(bdg.sum),
                                 str(bdg.budget),
                                 str(bdg.pk)])
        return data
