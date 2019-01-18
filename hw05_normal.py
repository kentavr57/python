import easy

__author__ = 'Валерий Сергеевич Коваленко'

# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"


def print_chois():
    print("Выберите нужное действие")
    print("1. Перейти в папку")
    print("2. Просмотреть содержимое текущей папки")
    print("3. Удалить папку")
    print("4. Создать папку")
    #return  #Сделайте ваш выбор или введите 'q' для завершения

print('*'*49)
print('*'*3, ' Консольная утилита для работы с папками ', '*'*3)
print('*'*49)
run = [easy.my_chdir, easy.my_listdir, easy.my_rmdir, easy.my_mkdir]
lrun = len(run)
uinp = -1
mess = 'Введите цифры от 1 до {} либо "q" для завершения работы'.format(lrun)
print_chois()
while True:
    uinp =input(f"{mess} $> ")
    if uinp == 'q' or uinp == 'quit' or uinp == 'exit':
        print('bye-bye')
        break
    try:
        ind = int(uinp)-1
        if ind > lrun-1 or ind < 0:
            print_chois()
        else:
            flag, mesj = run[ind]()
            print(mesj)
    except ValueError:
        print_chois()

"""
dname = input('Введите имя для новой папки: ')
flag, mess = easy.my_mkdir(dname)
print(mess)
dname = input('Введите имя для удаляемой папки: ')
flag, mess = easy.my_rmdir(dname)
print(mess)
flag, mess, list = easy.my_listdir()
print(mess)
dname = input('Введите имя папки в которую вы хотите перейти: ')
flag, mess = easy.my_chdir(dname)
print(mess)
"""
# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py
