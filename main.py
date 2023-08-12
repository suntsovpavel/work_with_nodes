
from workWithUser import *

def main():    
    workWithUser = WorkWithUser()  
    print("Для завершения работы введите 'stop'")
    stop_cycle = False
    while not stop_cycle:   # завершение цикла оператором return, не ищите stop_cycle = True...
              
        # выводим список доступных опций для ввода пользователем
        workWithUser.print_offer()             
    
        message_user = input()
        if message_user.lower() == 'stop':
            print('До свидания!')
            return    

        # обрабатываем сообщение, полученное от пользователя
        # здесь же вызываем инструменты работы с файлами
        workWithUser.handler_message_user(message_user)    
                   
main()    