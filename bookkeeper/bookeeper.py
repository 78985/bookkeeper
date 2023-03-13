"""
    # Исходник bookkeeper, являющийся
    # переходным звеном между внешним интерфейсом
    # и работой с самой БД.
    # Он не отвечает за эти действия напрямую, а только передаёт
    # команды и данные туда-сюда
"""
import os
from datetime import datetime

from bookkeeper.view.View import AbstractView, View
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'bookkeeper.db')


class Bookkeeper:
    """
    # Класс bookkeeper, являющийся
    # переходным звеном между внешним интерфейсом
    # и работой с самой БД.
    # Он не отвечает за эти действия напрямую, а только передаёт
    # команды и данные туда-сюда
    """

    def __init__(self,
                 view: AbstractView,
                 repository_type: type):

        self.view = view
        self.category_rep = repository_type[Category](
            db_file=db_path,
            cls=Category)
        self.categories = self.category_rep.get_all()
        self.view.set_categories(self.categories)
        self.view.set_ctg_adder(self.add_category)
        self.view.set_ctg_deleter(self.delete_category)
        self.view.set_ctg_checker(self.ctg_checker)
        self.view.set_ctg_updater(self.update_category)
        print('Вход в БД категорий обработан')

        self.budget_rep = repository_type[Budget](
            db_file=db_path,
            cls=Budget)
        self.view.set_bdg_modifier(self.modify_budget)
        print('Вход в БД бюджета обработан')

        self.expense_rep = repository_type[Expense](
            db_file=db_path,
            cls=Expense)
        self.expenses = self.expense_rep.get_all()
        self.view.set_expenses(self.expenses)
        self.update_budgets()
        self.view.set_exp_adder(self.add_expense)
        self.view.set_exp_deleter(self.delete_expense)
        self.view.set_exp_updater(self.update_expense)
        print('Вход в БД расходов обработан')


    def start_app(self) -> None:
        """

        Кусок для запуска приложения

        Returns
        -------

        """
        self.view.show_main_window()

    def ctg_is_empty(self) -> bool:
        """

        # Проверка, что БД категорий не пустой

        Returns
        -------

        """
        if self.categories is None:
            return True
        else:
            return False

    def ctg_checker(self, ctg_name: str) -> None:
        """

         # Проверка существования категории в БД

        Parameters
        ----------
        ctg_name

        Returns
        -------

        """
        if (not self.ctg_is_empty()) and \
                (ctg_name not in [c.name for c in self.categories]):
            self.view.set_expenses(self.expenses)
            self.view.set_categories(self.categories)
            print('Записи переданы в приложение')
            raise ValueError(f'Категории \'{ctg_name}\' не существует')

    def add_category(self, name: str, parent: str, childrens: str | None = None) -> None:
        """

        # Добавление категории в БД и в приложение

        Parameters
        ----------
        name
        parent
        childrens

        Returns
        -------

        """
        print('Вошли в функцию добавления категории в БД')

        if not self.ctg_is_empty():
            if name in [c.name for c in self.categories]:
                raise ValueError(f'Категория \'{name}\' уже существует')
        print('Проверили, что категория существует')
        print('Приступаем к проверке родителя')
        if (parent is not None) & (parent != ''):
            print(f'Введён непустой родитель {parent}.')
            if not self.ctg_is_empty():
                if parent not in [c.name for c in self.categories]:
                    raise ValueError(f'Родительской категории \'{parent}\' '
                                     f'не существует')

                parent_pk = self.category_rep.get_all(
                    where={'name': f'= \'{parent}\''})[0].pk
            else:
                parent_pk = None

        else:
            print(f'Введён пустой родитель {parent}')
            parent_pk = None

        print('Родитель установлен')

        ctg_obj = Category(name, parent_pk)
        print('Сформирован объект')
        self.category_rep.add(ctg_obj)
        print('Объект добавлен в БД')

        if (childrens is not None) & (childrens != ''):
            print('Приступаем к обработке детей')
            for child_name in childrens.split(' '):
                print(f'Рассматривается ребёнок {child_name}')
                self.ctg_checker(child_name)
                if (child_name == name) | (child_name == parent):
                    raise ValueError('Так делать нельзя!')
                print('Ребёнок не родитель для самого себя')
                child = self.category_rep.get_all(
                    where={'name': f'= \'{child_name}\''})[0]
                print(f'Получили класс объекта ребёнка: {str(child)}')
                child.parent = ctg_obj.pk
                print('Родитель ребёнка изменён')
                self.category_rep.update(child)
                print('Запись ребёнка в БД обновлена')
            print('Дети обработаны')
        print('Приступаем к обновлению списку категорий')
        self.categories = self.category_rep.get_all()
        for cats in self.categories:
            print(f'Имеется категория: {cats.name}')
        print('Список категорий отправляется в приложение')
        self.view.set_categories(self.categories)
        print('Процесс добавления категории завершён')
    def delete_category(self, ctg_name: str) -> None:
        """
         # Удаление категории из БД и приложения
        Parameters
        ----------
        ctg_name

        Returns
        -------

        """
        print(f'Приступаем к удалению категории {ctg_name}')
        self.ctg_checker(ctg_name)
        print('Проверено наличие категории')
        if self.ctg_is_empty():
            raise ValueError('Нельзя удалять из пустой таблицы!')
        ctg = self.category_rep.get_all(where={'name': f'= \'{ctg_name}\''})[0]
        print(f'Получен объект удаляемой категории: {str(ctg)}')
        print('Определим детей категории')
        childrens = ctg.get_subcategories(self.category_rep)
        if childrens == []:
            print('Удаляемая категория не имеет детей.\n'
                  'Перепривязка не нужна.')
        else:
            print('Удаляемая категория - родитель. \n'
                  'Приступаем к перепривязке.')
            for child in childrens:
                print(f'Рассматриваем ребёнка: {str(child)}')
                if child.parent == ctg.pk:
                    print('Обнаружен прямой наследник.')
                    child.parent = ctg.parent
                    print('Родитель изменён')
                    self.category_rep.update(child)
                    print('Запись ребёнка изменена в БД')

        print('Приступаем к перепривязке затрат')
        expenses_of_deleted_ctg = self.expense_rep.get_all(
            where={'category': f'= {ctg.pk}'})
        print(f'{expenses_of_deleted_ctg}')
        if (expenses_of_deleted_ctg != []) & (expenses_of_deleted_ctg is not None):
            print('Пройдена проверка на наличие объектов')
            for expense in expenses_of_deleted_ctg:
                print(f'Обнаружен расход: {str(expense)}')
                expense.category = ctg.parent
                print('Категория переназначена')
                self.expense_rep.update(expense)
                print('Запись расхода обновлена в БД')
        print('Приступаем к передаче новых данных')
        self.expenses = self.expense_rep.get_all()
        print('Записи о расходах обновлены')
        self.view.set_expenses(self.expenses)
        print('Запись о расходах отправлена в приложение')
        self.update_budgets()
        print('Запись бюджета обновлена')

        self.category_rep.delete(ctg.pk)
        print('Категория удалена из БД')
        self.categories = self.category_rep.get_all()
        print('Категории обновлены')
        self.view.set_categories(self.categories)
        print('Категории переданы в приложение')
        self.view.set_expenses(self.expenses)
        print('Расходы переданы в приложение')
        print('Удаление категории завершено')

    def update_category(self, ctg_name: str, parent: str, childrens: str = None) -> None:
        """
        # Обновление категории
        Parameters
        ----------
        ctg_name
        parent
        childrens

        Returns
        -------

        """
        print('Приступаем к обновлению категории')
        if self.ctg_is_empty():
            raise ValueError('Нельзя обновлять записи пустой таблицы!')
        self.delete_category(ctg_name)
        print('Категория удалена')
        self.add_category(ctg_name, parent, childrens)
        print('Категория восстановлена')
        print('Обновление категории завершено')

    def exp_is_empty(self) -> bool:
        """
        # Проверка, что БД категорий не пустая
        Returns
        -------

        """
        if self.expenses is None:
            return True
        else:
            return False
    def add_expense(self, amount: str, ctg_name: str, comm: str = '') -> None:
        """
        # Добавить расход
        Parameters
        ----------
        amount
        ctg_name
        comm

        Returns
        -------

        """
        print('Приступаем к добавлению расхода')
        try:
            amount = float(amount)
        except:
            raise ValueError('Некорректный ввод! Введите число.')
        if amount <= 0:
            raise ValueError('Некорректный ввод! Введите положительное число.')
        print('В поле расхода введено правильное число')
        if self.ctg_is_empty():
            self.add_category(name=ctg_name, parent=None)
            print('Список категорий был пуст. Введённая категория была добавлена в БД')
        self.ctg_checker(str(ctg_name))
        print('Введённая категория существует')
        ctg = self.category_rep.get_all(where={'name': f'= \'{str(ctg_name)}\''})[0]
        print('Получен полный класс введённой категории')
        print(str(ctg))
        new_expense = Expense(amount=amount, category=ctg.pk, comment=comm)
        print('Создан новый объект затраты')
        self.expense_rep.add(new_expense)
        print('Объект затраты добавлен в БД')
        self.expenses = self.expense_rep.get_all()
        print('Получены новые расходы')
        self.view.set_expenses(self.expenses)
        print('Расходы отправлены в приложение')
        self.update_budgets()
        print('Бюджет обновлён')
        print('Процедура добавления расходов завершена')
    def update_expense(self, pk: int, attrs: list[str], new_vals: list[str]) -> None:
        """
        # Изменим данные о затрате
        Parameters
        ----------
        pk
        attrs
        new_vals

        Returns
        -------

        """
        print('Приступаем к изменению расхода')
        if self.exp_is_empty():
            self.view.set_expenses(self.expenses)
            print('Записи переданы в приложение')
            raise ValueError('Нельзя изменять записи пустой таблицы!')
        print('Проверили, что есть что менять')
        expense = self.expense_rep.get(pk)[0]
        print('Получили объект расходов, который будем менять')
        if (attrs == []) | ('pk' in attrs):
            self.view.set_expenses(self.expenses)
            print('Записи переданы в приложение')
            raise ValueError('Так делать нельзя!')
        print('Убедились, что всё хорошо')
        for j in range(len(attrs)):
            field_name = attrs[j]
            field_val = new_vals[j]
            print(f'Сейчас меняем значение в поле {field_name} '
                  f'на величину {field_val} ')
            if field_name == 'category':
                print('Начинаем редактировать категорию')
                self.ctg_checker(field_val)
                field_val = self.category_rep.get_all(
                    where={'name': f'= \'{field_val}\''})[0].pk
                print('Получили новый ключ категории')

            if field_name == 'amount':
                print('Начинаем редактировать затрату')
                try:
                    field_val = float(field_val)
                except:
                    self.view.set_expenses(self.expenses)
                    print('Записи переданы в приложение')
                    raise ValueError('Некорректный ввод! Введите число.')
                if field_val <= 0:
                    self.view.set_expenses(self.expenses)
                    print('Записи переданы в приложение')
                    raise ValueError('Некорректный ввод! Введите положительное число.')
                print('Затрата введена корректная. Строка переведена во float')

            if field_name == 'expense_date':
                print('Начинаем редактировать дату затраты')
                try:
                    field_val = datetime.fromisoformat(field_val).isoformat(
                        sep='T', timespec='seconds')
                except:
                    self.view.set_expenses(self.expenses)
                    print('Записи переданы в приложение')
                    raise ValueError('Неправильный формат даты.')
                print('Дату ввели корректно. Передаём дальше')
            setattr(expense, field_name, field_val)
            print('Значение поля обновлено')
        setattr(expense, 'added_date', datetime.now().isoformat()[:19])
        print('Обновили поле с датой обновления записи')
        self.expense_rep.update(expense)
        print('Данные в БД обновлены')
        self.expenses = self.expense_rep.get_all()
        print('Записи в классе обновлены')
        self.view.set_expenses(self.expenses)
        print('Записи переданы в приложение')
        self.update_budgets()
        print('бюджет обновлён')
        print('Обновление данных расхода завершено')

    def delete_expense(self, pk: str) -> None:
        """
        # Удаление записи о расходах
        Parameters
        ----------
        pk

        Returns
        -------

        """
        print('Приступаем к удалению данных из расходов')
        if self.exp_is_empty():
            raise ValueError('Нельзя удалять записи пустой таблицы!')
        try:
            pk = int(pk)
        except:
            raise ValueError('Некорректный ввод!')
        if not isinstance(pk, int):
            raise ValueError('Что-то не так с форматом!')
        exp_for_delete = self.expense_rep.get(pk)
        print(exp_for_delete)
        if (exp_for_delete == []) | (exp_for_delete is None):
            raise ValueError('Такой записи нет - удалять нечего!')
        self.expense_rep.delete(pk)
        self.expenses = self.expense_rep.get_all()
        self.view.set_expenses(self.expenses)
        self.update_budgets()
        print('Расход удалён')

    def update_budgets(self) -> None:
        """
        # Обновляем информацию о бюджете везде
        Returns
        -------

        """
        print('Приступаем к обновлению бюджета')
        if self.budget_rep.get_all() is None:
            print('Активных записей нет')
        else:
            print('Найдены активные записи')
            for budget in self.budget_rep.get_all():
                budget.update_spented_sum(self.expense_rep)
                print('Трата в бюджете обновлена')
                self.budget_rep.update(budget)
                print('Обновлена запись в БД')
        self.budgets = self.budget_rep.get_all()
        print('Записи бюджетов в классе обновлены')
        self.view.set_budgets(self.budgets)
        print('Записи бюджетов отправлены в приложение')

    def modify_budget(self, pk: int | None, new_budget_val: str, time: str) -> None:
        """
        # Модифицируем бюджет (т.е. изменяем данные)
        Parameters
        ----------
        pk
        new_budget_val
        time

        Returns
        -------

        """
        if new_budget_val == '':
            print('Удалена запись о бюджете. Удаляем информацию')
            if (pk is not None) & (pk != ''):
                self.budget_rep.delete(pk)
                print('Запись удалена')
            self.update_budgets()
            print('Данные о бюджетах обновлены')
        else:
            try:
                new_budget_val = float(new_budget_val)
            except ValueError:
                self.update_budgets()
                print('Записи бюджета обновлены')
                raise ValueError('Неправильный ввод! Введите число.')
            if new_budget_val < 0:
                self.update_budgets()
                print('Записи бюджета обновлены')
                raise ValueError('Неправильный ввод! Введите положительное число.')

            print('Ввод корректен')

            if (pk is None) | (pk == ''):
                budget = Budget(budget=new_budget_val, time=time)
                print('Создана новая запись')
                self.budget_rep.add(budget)
                print('Запись добавлена в БД')
            else:
                budget = self.budget_rep.get(pk)[0]
                print('Запись по ключу получена')
                budget.budget = new_budget_val
                self.budget_rep.update(budget)
                print('Запись в БД обновлена')
        self.update_budgets()
if __name__ == '__main__':
    view = View()
    bookkeeper_app = Bookkeeper(view, SQLiteRepository)
    bookkeeper_app.start_app()
