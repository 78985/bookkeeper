"""Всё, что отвечает за интерфейс и внешнюю логику удаления"""
from PyQt6 import QtWidgets


class DeleteLine(QtWidgets.QLineEdit):
    """
    # Класс, описывающий строку,
    # что удаляет записи расходов из таблицы
    """

    def __init__(self, expense_deleter=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expense_deleter = expense_deleter
        self.setPlaceholderText('Введи ключик расхода на удаление')
        self.textChanged.connect(self.text_is_changing)

    def text_is_changing(self) -> None:
        """
        # Обработка события начала изменения текста - ожидаем обработки окончания ввода
        """
        self.textChanged.disconnect(self.text_is_changing)
        print('Готовы к удалению. Ожидаем завершения ввода')
        self.editingFinished.connect(self.delete_expense)

    def delete_expense(self) -> None:
        """
        # Обрабатывается окончание редактирования -
        # удаляем расход из таблицы расходов
        """
        print('Ввод завершён. Начинаем удалять')
        self.editingFinished.disconnect(self.delete_expense)
        print('Отключили соединение с предыдущей командой')
        pk = self.displayText()
        print(f'Получили текст. pk = {pk}')
        print('Ключ переведён из текста в int')
        self.clear()
        self.textChanged.connect(self.text_is_changing)

        self.expense_deleter(pk)
        print('Расход удалён')
