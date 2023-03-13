"""
Кусок таблицы, отвечающий за вывод расходов и
работу пользователя с ними
"""
from PyQt6 import QtWidgets
from bookkeeper.models.expense import Expense


class ExpenseTable(QtWidgets.QTableWidget):
    """
    #Здесь создаётся класс таблицы.
    # Он отличается тем, что все данные о настройке
    # таблицы мы вытащим в отдельное
    # место, а потом просто воткнём в приложение.
    # Также тут собрана вся логика работы с
    # данными в таблице
    # которые потом отправляются на обработку в БД и далее.
    """

    def __init__(self,
                 expenses_updater=None,
                 ctg_pk_2_name=None,
                 rws: int = 50,
                 clmns: int = 5,
                 header_text: str = 'Дата Сумма Категория Комментарий Ключик',
                 *args, **kwargs) -> None:
        super().__init__(*args, *kwargs)
        self.expenses_updater = expenses_updater
        self.ctg_pk_2_name = ctg_pk_2_name

        self.setColumnCount(clmns)
        self.setRowCount(rws)
        self.setHorizontalHeaderLabels(header_text.split())
        for j in range(clmns):
            self.resizeColumnToContents(j)
        self.SetTableData()
        self.expenses_attrs = {0: 'expense_date',
                               1: 'amount',
                               2: 'category',
                               3: 'comment', 4
                               : 'pk'}
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)

        self.cellDoubleClicked.connect(self.cell_double_clicked)

    def SetTableData(self, data: list[list[str]] = None) -> None:
        """
         # Функция заполнения полей таблицы
        Parameters
        ----------
        data

        Returns
        -------

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
        """# Обработка события двойного щелчка - ожидаем обработки редактирования"""
        print('Начали ожидать конца редактирования')
        self.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row, column) -> None:
        """    # Обрабатывается окончание редактирования -
    # составляем новые параметры записи"""
        print('Приступили к обработке события после конца редактирования')
        self.cellChanged.disconnect(self.cell_changed)
        print('Отключили кнопку, чтобы не было дублирования')
        pk = self.data[row][-1]
        print('Определили ключ записи')
        new_val = self.item(row, column).text()
        print('Определили новые параметры затраты')
        attr = self.expenses_attrs[column]
        print('Вернули имя атрибута, которому меняли значение')
        print('Передаём данные в обработчик обновлений затрат')
        self.expenses_updater(pk, [attr], [new_val])

    def set_expenses(self, expenses: list[Expense]) -> None:
        """
        # Запись в таблицу расходов из БД
        Parameters
        ----------
        expenses

        Returns
        -------

        """
        self.expenses = expenses
        self.data = self.expenses_to_data(self.expenses)
        self.clearContents()
        self.SetTableData(self.data)

    def expenses_to_data(self, expenses: list[Expense] | None) -> list[list[str]]:
        """
            # Конвертер из типов характерных для Expenses
    # в строки
        Parameters
        ----------
        expenses

        Returns
        -------

        """
        data = []
        if expenses is None:
            data = [['Empty', 'Empty', 'Empty', 'Empty', 'Empty']]
        else:
            for expense in expenses:
                item = [str(expense.expense_date),
                        str(expense.amount),
                        str(self.ctg_pk_2_name(expense.category)),
                        str(expense.comment),
                        str(expense.pk)]
                data.append(item)
        return data
