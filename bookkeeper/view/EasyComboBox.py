"""Класс для простого создания и настройки выпадающего списка"""
from PyQt6 import QtWidgets


class EasyComboBox(QtWidgets.QComboBox):
    """Класс для простого создания и настройки выпадающего списка"""

    def __init__(self, cur_text: str = 'Empty', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.set_items()
    def set_items(self, text_for_items: list[str] = ['empty']) -> None:
        """
        # Составляем начинку выпадающего списка
        Parameters
        ----------
        text_for_items

        Returns
        -------

        """
        self.clear()
        print('В теории, список должен был очиститься')
        super().clear()
        print('Совсем мощно должен был очиститься')
        if (isinstance(text_for_items, str)) | (text_for_items == []):
            raise ValueError('Неверный ввод!')
        for name in text_for_items:
            print(f'Добавлено окошко {name}')
            self.addItem(name)