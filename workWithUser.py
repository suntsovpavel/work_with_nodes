
from tasks import Task
from workWithFiles import *

# using global parameters:
task = Task.NONE       # текущая операция
idNote = None        # id заметки
title = None        # наименование заметки
item = None         # содержимое заметки             
# параметры выборки по дате:
        # Для формирования выборки укажите границы дат слева и справа, через запятую в формате "%m-%d-%Y %H:%M:%S"')        
        # Если дата интервала не установлена, введите no')
        # Примеры: 08-01-2023 17:47:35, 08-10-2023 23:59:59')
        #         no, 08-10-2023 23:59:59')
        #         no, no  (будут выведены все заметки)')  
datetime_left = None
datetime_right= None       

# Возвращаем параметры в исходное состояние
def initial_state():
    global task, idNote, title, item, list_notes, is_sample_data, datetime_left, datetime_right
    task = Task.NONE       # текущая операция
    idNote = None        # id заметки
    title = None        # наименование заметки
    item = None         # содержимое заметки    
    ddatetime_left = None   # параметры выборки по дате
    datetime_right= None     

# Парсим строку, введенную пользрователем, и получаем  параметры выборки по дате  datetime_left,datetime_right      
# Возвращаем None, если парсинг прошел успешно,
# либо сообщение об ошибке    
def parse_string_datetime_limits(string):
    errorMessage = None
    global datetime_left, datetime_right
    splitted = string.split(',')   
    if len(splitted) != 2:
        return 'сплит по запятой должен дать 2 элемента'
    
    parsed_left = splitted[0].strip()
    if parsed_left.lower() == 'no':
        datetime_left = None
    else:
        result = parse_datetime(parsed_left)
        if result == None:  # ошибка парсинга
            return 'не спарсено выражение ' + parsed_left
        datetime_left = result
            
    parsed_right = splitted[1].strip()
    if parsed_right.lower() == 'no':
        datetime_right = None
    else:
        result = parse_datetime(parsed_right)
        if result == None:  # ошибка парсинга
            return 'не спарсено выражение ' + parsed_right
        datetime_right = result                        
    return None                        

# выводим список доступных опций для ввода пользователем
def print_offer():
    global task, title
    
    if task == Task.NONE:   #задача не выбрана
        print('\nВыберите операцию:')
        print('1. Вывести список заметок')    
        print('2. Создать новую заметку')
        print('3. Отредактировать заметку (задать id)')
        print('4. Просмотреть заметку (задать id)')
        print('5. Удалить заметку (задать id)')            
        
    elif task == Task.GET_LIST:  
        print('Для формирования выборки заметок укажите границы дат слева и справа, через запятую в формате "%m-%d-%Y %H:%M:%S"')        
        print("Если дата не установлена, введите 'no'")
        print('Примеры: 08-01-2023 17:47:35, 08-10-2023 23:59:59')
        print('         no, 08-10-2023 23:59:59')
        print('         no, no  (будут выведены все заметки)')                               
        
    elif task == Task.ADD:  # Создать новую заметку    
        if title == None:
            print('Введите название заметки:')
        else:
            print('Введите текст заметки:')     
            
    elif task == Task.EDIT:    # Отредактировать заметку            
        if idNote == None:       
            print('Введите id заметки для редактирования. Посмотреть id заметок можно в выборе п.1')    
        else:
            print('введите новое содержимое заметки:')                         
            
    elif task == Task.GET:  # Просмотр содержимого заметки            
        print('Введите id заметки для просмотра. Посмотреть id заметок можно в выборе п.1')     
                
    elif task == Task.DELETE:  # Просмотр содержимого заметки                  
        print('Введите id заметки для удаления. Посмотреть id заметок можно в выборе п.1') 
            
# обработчик сообщения, введенного пользователем        
            
def handler_message_user(message_user):
    global task, idNote, title, item
    
    if message_user == '':
        print('Введена пустая строка')  
        return
    
    if task == Task.NONE:   #задача не выбрана
        if message_user == '1':
            task = Task.GET_LIST
        elif message_user == '2':
            task = Task.ADD
        elif message_user == '3':
            task = Task.EDIT
        elif message_user == '4':
            task = Task.GET        
        elif message_user == '5':            
            task = Task.DELETE                
        else:
            print('Некорректный ввод')
            
    elif task == Task.GET_LIST:  
        errorMessage = parse_string_datetime_limits(message_user)
        if  errorMessage != None:
            print('Ошибка ввода данных: ' + errorMessage)             
        else:            
            list_notes, errorMessage = get_notes(datetime_left, datetime_right)
            if errorMessage != None:
                
                print('Ошибка get_notes: ' + errorMessage)            
            else:    
                if len(list_notes) == 0:
                    print('заметок нет')                                         
                else:                                     
                    print('Список заметок (отсортирован по id):')
                    for el in  list_notes:
                        print(f"id:{el['id']}, '{el['title']}', создана: {el['datetime']}")             
            initial_state()     # возвращаем параметры в исходное состояние        
            
    elif task == Task.ADD:  # Создать новую заметку            
        # Ожидаем наименование либо содержимое заметки         
        if title == None:
            title =  message_user
        else:
            item =  message_user
            
            # Вызываем функцию работы с файлами            
            errorMessage  = handler_files(task, title, item, idNote)
            if errorMessage == None:
                print('заметка успешно создана')                                          
                initial_state()      # возвращаем параметры в исходное состояние   
            else:
                print(errorMessage)   
                 
    elif task == Task.EDIT:    # Отредактировать заметку    
        list_notes, errorMessage = get_notes(None, None)
        if errorMessage != None:
            print('Ошибка get_notes: ' + errorMessage)            
        else:    
            if idNote == None:                   
                for el in list_notes:
                    if message_user == str(el['id']):                        
                        idNote = el['id']
                        print(f'Выбранная заметка: id = {idNote}')
                        print(f"Заголовок(название): {el['title']}")
                        print(f"Содержимое: {el['item']}")
                        print(f"Дата-время создания: {el['datetime']}")
                        break
                if idNote == None:
                    print('Неверно указан id')                                   
            else:
                # Редактируем только содержимое заметки, название не трогаем
                item = message_user
                
                # Вызываем функцию работы с файлами            
                errorMessage  = handler_files(task, title, item, idNote)
                if errorMessage == None:
                    print('заметка успешно отредактирована')                                          
                    initial_state()     # возвращаем параметры в исходное состояние        
                else:
                    print(errorMessage)    
                
    elif task == Task.GET:     
        list_notes, errorMessage = get_notes(None, None)
        if errorMessage != None:
            print('Ошибка get_notes: ' + errorMessage)            
        else:                      
            found = False                          
            for el in list_notes:
                if message_user == str(el['id']):
                    print('Выбранная заметка: id = ' + message_user)
                    print(f"Заголовок(название): {el['title']}")
                    print(f"Содержимое: {el['item']}")
                    print(f"Дата-время создания: {el['datetime']}")
                                    
                    initial_state() # возвращаем параметры в исходное состояние
                    found = True
                    break
            if not found:
                print('Неверно указан id')    
            
    elif task == Task.DELETE:    
        list_notes, errorMessage = get_notes(None, None)
        if errorMessage != None:
            print('Ошибка get_notes: ' + errorMessage)            
        else:               
            found = False
            for el in list_notes:
                if message_user == str(el['id']):
                    found = True
                    idNote = el['id']
                    
                    # Вызываем функцию работы с файлами            
                    errorMessage  = handler_files(task, title, item, idNote)
                    if errorMessage == None:
                        print('заметка успешно удалена')                          
                        initial_state() # возвращаем параметры в исходное состояние        
                    else:
                        print(errorMessage)                    
                    break
            if not found:
                print('Неверно указан id')              
            
                               
