__author__ = 'Валерий Сергеевич Коваленко'
# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.
import os
from shutil import copy
from sys import argv
print('sys.argv = ', argv)


def print_help():
    print("help - получение справки")
    print("mkdir <dir_name> - создание директории")
    print("ping <ip_address> - системная ping")
    print("cp <file_name> [<new_file_name>]- создает копию указанного файла")
    print("rm|del <file_name> - удаляет указанный файл ")
    print("cd <full_path or relative_path> - меняет текущую директорию на указанную")
    print("ls - отображение полного пути текущей директории")



def make_dir():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.mkdir(dir_path)
        print('директория {} создана'.format(dir_name))
    except FileExistsError:
        print('директория {} уже существует'.format(dir_name))


def ping():
    if not dir_name:
        print("Необходимо указать ip адрес вторым параметром")
        return
    rstr = 'ping {}'.format(dir_name)
    try:
        os.system(rstr)
    except:
        print(f'Проблемма с запуском пинга')

def ls():
    print(os.getcwd())


def cp():
    if not dir_name:
        print("Необходимо указать имя файла вторым параметром")
        return
    d_path = os.getcwd()
    if not cp_name:
        new_name = 'copy_{}'.format(dir_name)
    else:
        new_name = cp_name
    try:
        copy(os.path.join(d_path, dir_name),  os.path.join(d_path, new_name))
        print(f'Файл скопирован успешно, новое имя {new_name}')
    except FileNotFoundError:
        print(f'Нет такого файла {dir_name}')


def cd2():
    if not dir_name:
        print("Необходимо указать имя папки вторым параметром")
        return
    if dir_name == '..' or (os.name == 'nt' and dir_name[1] == ':') or (os.name == 'posix' and dir_name[0] == '/'):
        dpath = dir_name
    else:
        dpath = os.path.join(os.getcwd(), dir_name)
    try:
        os.chdir(dpath)
        print('Успешно перешел в папку {}'.format(dir_name))
    except FileNotFoundError:
        print('Не найдено папки {}'.format(dir_name))

def cd():
    if not dir_name:
        print("Необходимо указать имя папки вторым параметром")
        return
    if dir_name == '..' or (os.name == 'nt' and dir_name[1] == ':') or (os.name == 'posix' and dir_name[0] == '/'):
        dpath = dir_name
    else:
        dpath = os.path.join(os.getcwd(), dir_name)
    try:
        os.chdir(dpath)
        print('Успешно перешел в папку {}'.format(dir_name))
    except FileNotFoundError:
        print('Не найдено папки {}'.format(dir_name))


def rm():
    if not dir_name:
        print("Необходимо указать имя файла вторым параметром")
        return
    dpath = os.path.join(os.getcwd(), dir_name)
    ans = input(f"Вы уверены что хотите удалить файл {dpath}  Y/N[Д/Н]")
    ans =ans[0].lower()
    if ans == 'y' or ans == 'д':
        try:
            os.remove(dpath)
            print(f"Файл удален: {dir_name}")
        except FileNotFoundError:
            print(f"Не существует такого файла: {dir_name}")
        except OSError:
            print(f"Ошибка удаления")
    else:
        print(f"Удаление отменено")


do ={
    "help": print_help,
    "mkdir": make_dir,
    "ping": ping,
    "ls": ls,
    "cp": cp,
    "cd": cd,
    "rm": rm,
    "del": rm
}
try:
    cp_name = argv[3]
except IndexError:
    cp_name = None

try:
    dir_name = argv[2]
except IndexError:
    dir_name = None

try:
    key = argv[1]
except IndexError:
    key = None


if key:
    if do.get(key):
        do[key]()
    else:
        print("Задан неверный ключ")
        print("Укажите ключ help для получения справки")