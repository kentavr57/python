import os
from shutil import copy
from sys import argv


def my_chdir(dname=''):
    if not dname:
        dname = input('Введите имя папки в которую вы хотите перейти: ')
        if not dname:
            return False, 'Не задано имя папки'
    if ':' or '..' in dname: #абсолютный путь либо к родителю
        dpath = dname
    else:
        dpath = os.path.join(os.getcwd(), dname)
    try:
        os.chdir(dpath)
        return True, 'Успешно перешел в папку {}'.format(dname)
    except FileNotFoundError:
        return False, 'Не найдено папки {}'.format(dname)


def my_listdir(f=False):
    dpath = os.getcwd()
    try:
        lst = os.listdir(dpath)
        if f:
            lst = [x for x in lst if os.path.isdir(os.path.join(dpath, x))]
            if len(lst) == 0:
                return False, "В дирректории {} нет папок".format(dpath)
        if len(lst) == 0:
            return False, "Папка пуста".format(dpath)
        return True, '\n'.join(x for x in lst if os.path.isdir(os.path.join(dpath, x)))+'\n'+'\n'.join('.....'+x for x in lst if os.path.isfile(os.path.join(dpath, x)))
    except:
        return False, "Такой папки не существует: {}".format(dpath)


def my_mkdir(dname=''):
    if not dname:
        dname = input('Введите имя для новой папки: ')
        if not dname:
            return False, 'Не задано имя папки'
    if ':' in dname: #абсолютный путь
        dpath = dname
    else:
        dpath = os.path.join(os.getcwd(), dname)
    try:
        os.mkdir(dpath)
        return True, "Папка успешна создана: {}".format(dpath)
    except FileExistsError:
        return False,"Папка существует: {}".format(dpath)
    except:
        return False, "Какаято ошибка при создании папки"

def my_rmdir(dname=''):
    if not dname:
        dname = input('Введите имя для удаляемой папки: ')
        if not dname:
            return False, 'Не задано имя папки'
    if ':' in dname:  # абсолютный путь
        dpath = dname
    else:
        dpath = os.path.join(os.getcwd(), dname)
    try:
        os.rmdir(dpath)
        return True, "Папка успешна удалена: {}".format(dpath)
    except FileNotFoundError:
        return False, "Такой папки не существует: {}".format(dpath)
    except OSError:
        return False, "Папка {} не пуста".format(dpath)