from enum import Enum
     
class Task(Enum):
    NONE = 0,      # задача не выбрана 
    GET_LIST = 1,   # Вывести список заметок
    ADD = 2,        # создаем новую заметку
    EDIT = 3,     # редактируем заметку
    GET = 4,        # читаем заметку
    DELETE = 5      # удаляем заметку