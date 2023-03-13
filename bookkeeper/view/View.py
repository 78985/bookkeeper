"""
View отвечает за данные и вывод их от и к пользователю.
Abstract View - абстрактная архитектура
"""
import sys
from typing import Protocol
from collections.abc import Callable
from PyQt6 import QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from bookkeeper.view.Window import BookkeeperWindow


class AbstractView(Protocol):
    """
    Абстрактная архитектура
    """

    def show_main_window(self) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_categories(self, ctg: list[Category]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_expenses(self, ctg: list[Expense]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_budgets(self, ctg: list[Budget]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_ctg_adder(self, handler: Callable[[str, str], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_ctg_deleter(self, handler: Callable[[str], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_ctg_checker(self, handler: Callable[[str], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_ctg_updater(self, handler: Callable[[str, str, str | None], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_bdg_modifier(self, handler: Callable[['int | None', str, str], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_exp_adder(self, handler: Callable[[str, str, str], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_exp_deleter(self, handler: Callable[[str], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass


    def set_exp_updater(self, handler: Callable[[int, list[str], list[str]], None]) -> None:
        """Предобъявленная абстрактная функция"""
        pass




def handle_error(widget, handler):
    """
    Функция, которая позволяет проверить,
    что присваивание к местной функции функции из прослойки
    прошло успешно.Если нет - вывести ошибку.
    И ещё вывести ошибку, если в присвоенной функции произошла обработка
    исключения.
    Parameters
    ----------
    widget
    handler

    Returns
    -------

    """

    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValueError as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))

    return inner


class View:
    """
    View отвечает за данные и вывод их от и к пользователю.
    """
    categories: list[Category] = [Category(name='Empty_Cat')]

    def __init__(self):
        print('Запуск приложения начат')
        self.app = QtWidgets.QApplication(sys.argv)

        self.main_window = BookkeeperWindow(self.categories,
                                            self.add_expense,
                                            self.update_expense,
                                            self.delete_expenses,
                                            self.ctg_pk_2_name,
                                            self.add_category,
                                            self.update_category,
                                            self.delete_category,
                                            self.modify_budget)
        print('Окно запущено')
        self.main_window.resize(1200, 700)
        self.main_window.setWindowTitle('Чёрная Бухгалтерия')

    def show_main_window(self) -> None:
        """ # Функция запуска основного окна"""
        self.main_window.show()
        print('Приложение запущено')
        print(f'Application ends with exit status {self.app.exec()}')
        sys.exit()


    def set_categories(self, ctg: list[Category]) -> None:
        """ Передача категорий в интерфейс"""
        self.categories = ctg
        self.main_window.ExpenseAndCategoryEdit.set_categories(self.categories)

    def ctg_pk_2_name(self, pk: int | None) -> str:
        """ Имя категории по её ключу"""
        if pk is None:
            return 'Empty'
        else:
            name = [c.name for c in self.categories if int(c.pk) == int(pk)]
            if len(name):
                return str(name[0])

    def set_ctg_updater(self, handler) -> None:
        """ Устанавливает метод изменения категории"""
        self.ctg_updater = handle_error(self.main_window, handler)


    def set_ctg_adder(self, handler) -> None:
        """ Устанавливает метод добавления категории"""
        self.ctg_adder = handle_error(self.main_window, handler)


    def set_ctg_deleter(self, handler) -> None:
        """ Устанавливает метод удаления категории"""
        self.ctg_deleter = handle_error(self.main_window, handler)


    def set_ctg_checker(self, handler) -> None:
        """ Устанавливает метод проверки существования категории"""
        self.ctg_checker = handle_error(self.main_window, handler)

    def add_category(self, name, parent, children) -> None:
        """ Для выполнения добавления категории """
        self.ctg_adder(name, parent, children)

    def update_category(self, name, parent, children) -> None:
        """ Для выполнения обновления категории"""
        self.ctg_updater(name, parent, children)


    def delete_category(self, ctg_name: str) -> None:
        """ Для выполнения удаления категории"""
        self.ctg_deleter(ctg_name)

    def set_expenses(self, exps: list[Expense]) -> None:
        """ Передача расходов в интерфейс"""
        self.expenses = exps
        self.main_window.ExpensesTable.set_expenses(self.expenses)

    def set_exp_adder(self, handler) -> None:
        """ Устанавливает метод добавления траты"""
        self.exp_adder = handle_error(self.main_window, handler)


    def set_exp_deleter(self, handler) -> None:
        """ Устанавливает метод удаления траты"""
        self.exp_deleter = handle_error(self.main_window, handler)


    def set_exp_updater(self, handler) -> None:
        """ Устанавливает метод изменения траты"""
        self.exp_updater = handle_error(self.main_window, handler)

    def add_expense(self, amount: str, ctg_name: str, comment: str = "") -> None:
        """Добавление траты"""
        self.exp_adder(amount, ctg_name, comment)


    def delete_expenses(self, pk: str) -> None:
        """ Удаление траты"""
        dlg = QtWidgets.QMessageBox(self.main_window)
        dlg.setWindowTitle('Удаление')
        dlg.setText('Удалить выбранный расход?')
        dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes |
                               QtWidgets.QMessageBox.StandardButton.No)
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Question)

        button = dlg.exec()

        if button == QtWidgets.QMessageBox.StandardButton.Yes:
            self.exp_deleter(pk)

    def update_expense(self, pk, attr, new_val) -> None:
        """ Обновление траты"""
        self.exp_updater(pk, attr, new_val)


    def set_budgets(self, budgets: list[Budget]) -> None:
        """ Передача бюджетов в интерфейс"""
        self.budgets = budgets
        self.main_window.BudgetTable.set_budgets(self.budgets)


    def set_bdg_modifier(self, handler) -> None:
        """ Устанавливает метод изменения бюджета"""
        self.bdg_modifier = handle_error(self.main_window, handler)


    def modify_budget(self, pk: int, new_limit: str, period: str) -> None:
        """ Для модификации данных бюджета"""
        self.bdg_modifier(pk, new_limit, period)
