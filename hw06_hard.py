__author__ = 'Валерий Сергеевич Коваленко'
# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла

import os

class Workers():
    def __init__(self, str_from_file=''):
        if not str_from_file:
            #raise ValueError
            pass
        str_from_file = str_from_file.replace('\n', '').split()
        self.i = str_from_file[0]
        self.f = str_from_file[1]
        self.s = int(str_from_file[2])
        self.d = str_from_file[3]
        self.n = int(str_from_file[4])

    hours = 0
    salary = 0

    def s_fio(self):
        return '{} {}.'.format(self.f, self.i[0])

    def n_fio(self):
        return '{} {}'.format(self.i, self.f)

    def set_salary(self):
        if self.hours == self.n:
            self.salary = self.s
        elif self.hours < self.n:
            self.salary = self.s*self.hours/self.n
        else:
            self.salary = self.s/self.n*2*(self.hours-self.n)+self.s
        self.salary = round(self.salary, 2)

    def set_hours(self, str_from_file=''):
        if str_from_file and self.i in str_from_file and self.f in str_from_file:
            str_from_file = str_from_file.replace('\n', '').split()
            self.hours = int(str_from_file[2])
            self.set_salary()


#Прочитаем data/workers+
with open(os.path.join('data', 'workers+'), 'r', encoding="utf8") as f:
    workers = f.readlines()
#Прочитаем data/hours_of+
with open(os.path.join('data', 'hours_of+'), 'r', encoding="utf8") as f:
    hours = f.readlines()

workers = workers[1:]
hours = hours[1:]

workers = [Workers(x) for x in workers] #инициализируем классы
[[x.set_hours(st) for x in workers]for st in hours] #присваеваем часы и рассчитываем зарплату

print("Расчетная ведомость")
print("    {:<15} {:<10} {:<14} {:<10}  Подпись".format("ФИО", "Оклад", "Часы норм/отр", "Зарплата"))
print('\n'.join(["{:<3} {:<15} {:<10} {}/{:<10} {:<10}  _____________".format(i+1, x.s_fio(), x.s, x.n, x.hours, x.salary) for i, x in enumerate(workers)]))
