__author__ = 'Валерий Сергеевич Коваленко'
# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.
print(">>> скрипт, создающий директории dir_1 - dir_9")
import os

for i in range(1, 10):
    dpath = os.path.join(os.getcwd(), "dir_{}".format(i))
    try:
        os.mkdir(dpath)
        print(f"Дирректория создана: {dpath}")
    except FileExistsError:
        print(f"Дирректория существует: {dpath}")

print(">>> скрипт, удаляющий директории dir_1 - dir_9")
input("Нажмите ENTER для удаления")

for i in range(1, 10):
    dpath = os.path.join(os.getcwd(), "dir_{}".format(i))
    try:
        os.rmdir(dpath)
        print(f"Дирректория удалена: {dpath}")
    except FileNotFoundError:
        print(f"Такой дирректории не существует: {dpath}")
    except OSError:
        print(f"Дирректория {dpath} не пуста")



# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.
print(">>> отображающий папки текущей директории")
dpath = os.getcwd()
try:
    lst = os.listdir(dpath)
    lst = [x for x in lst if os.path.isdir(os.path.join(dpath, x))]
    if len(lst) > 0:
        print("Список папок в дирректории {}".format(dpath), '\n', '\n'.join(x for x in lst))
    else:
        print(f"В дирректории {dpath} нет папок")
except:
    print(f"Такой дирректории не существует: {dpath}")



# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.
print(">>> 3.1 копию файла с помошью системных утилит")
dpath = os.getcwd()
fpath = __file__
cpath = os.path.join(dpath, "copy_{}".format(os.path.basename(__file__)))
if os.name == 'nt':
    rstr = 'copy "{}" "{}"'.format(fpath, cpath)
else:
    rstr = 'cp {} {}'.format(fpath, cpath)
try:
    os.system(rstr)
    print(f'Файл скопирован успешно, новое имя copy_{os.path.basename(__file__)}')
except:
    print(f'Проблемма с копированием файла {__file__}')

print(">>> 3.2 копию файла с помошью import shutil")
from shutil import copy
from sys import argv
dpath = os.getcwd()
fpath = argv[0]
cpath = os.path.join(dpath, "copy_{}".format(os.path.basename(argv[0])))
try:
    copy(fpath, cpath)
    print(f'Файл скопирован успешно, новое имя copy_{os.path.basename(__file__)}')
except FileNotFoundError:
    print(f'Проблемма с копированием файла {__file__}')

