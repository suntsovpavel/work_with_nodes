
from tasks import Task
import json, os
from datetime import datetime

path = 'notes/'

# парсим строку с данными datetime в определенном формате
# если не удалось распарсить, возвращаем None
def parse_datetime(string):
    try:
        result = datetime.strptime(string, "%m-%d-%Y %H:%M:%S")       
    except Exception:  
        return None
    return result                

# читаем файлы и формируем выборку заметок по крайним датам
# Результат: список словарей { id, title, item, datatime }
def get_notes(date_min: datetime,   # параметры выборки
              date_max: datetime):
    errorMessage = None
    result = []
    list_names_item = os.listdir(path)
    for one in list_names_item:        
        if os.path.isfile(path + one):       
            try:                
                f = open(path + one, 'r', encoding='utf-8')
                note = json.load(f)
                                
                #Проверяем параметры выборки
                if date_min != None and parse_datetime(note['datetime']) < date_min:
                    continue
                if date_max != None and parse_datetime(note['datetime']) > date_max:
                    continue
                result.append(note)
            except Exception:      
                errorMessage = 'ошибка чтения файла ' + path + one
            finally:
                f.close()            
    return result, errorMessage  
    
def handler_files(task: Task,  # see enum Task
                  title: str, # заголовок заметки
                  item: str,     # содержимое заметки
                  idNote: int):  # id заметки для поиска среди уже созданных 
    errorMessage = None
    if task == Task.ADD:  # Создать новую заметку    
        note = {}        
        note['id'] = 0  # по умолчанию
        
        # для получения id новой заметки просматриваем уже созданные:        
        notes, errorMessage = get_notes(None, None)     #(None, None): получить все заметки
        if errorMessage != None:
            return  errorMessage
        
        # print(f'notes = {notes}')
        if len(notes) > 0:        
            id_max = 0
            for one in notes:
                if one['id'] > id_max:
                    id_max = one['id']
            # новая заметка получает id, следующий за наибольшим id среди уже созданных         
            note['id'] = id_max + 1                   
        
        note['title'] = title
        note['item'] = item
        note['datetime'] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            
        # Формируем файл с именем id
        namefile = str(note['id']) + '.json'
        try:
            with open(path + namefile, 'w', encoding='utf-8') as fw:
                json.dump(note, fw)                  
        except Exception :
            errorMessage = 'не удалось создать файл ' + namefile
            
    if task == Task.EDIT:   # редактируем заметку   
        notes, errorMessage = get_notes(None, None)
        if errorMessage != None:
            return  errorMessage
        
        found = False
        for el in notes:
            if idNote == el['id']:
                # Выполняем перезапись файла с новым содержимым item
                el['item'] = item
                el['datetime'] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                namefile = str(idNote) + '.json'
                try:
                    with open(path + namefile, 'w', encoding='utf-8') as fw:
                        json.dump(el, fw)                  
                except Exception :
                    errorMessage = 'не удалось создать файл ' + namefile        
                found = True                    
                break    
        if not found:
            errorMessage = 'передан некорректный idNote = ' + str(idNote)            
            
    if task == Task.DELETE:            
        notes, errorMessage = get_notes(None, None)
        if errorMessage != None:
            return  errorMessage
        found = False
        for el in notes:
            if idNote == el['id']:
                namefile = str(idNote) + '.json'
                try:
                    os.remove(path + namefile)
                except Exception:
                    errorMessage = 'не удалось удалить файл ' + namefile        
                found = True                    
                break                       
                
        if not found:
            errorMessage = 'передан некорректный idNote = ' + str(idNote)                      
    return  errorMessage