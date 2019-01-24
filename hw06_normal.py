__author__ = 'Валерий Сергеевич Коваленко'
# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать 
# в неограниченном кол-ве классов свой определенный предмет. 
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика 
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе


class People:
    def __init__(self, fio={"F": "", "I": "", "O": ""}, fm=1, parent={"f": "", "m": ""}, bd="" ):
        self.fio = fio
        self.parent = parent
        self.bd = bd
        self.fm = fm

    def sFIO(self):
        return "{} {}.{}.".format(self.fio['F'], self.fio['I'][0], self.fio['O'][0])


class Student(People):
    def __init__(self, people,  cls=""):
        self.cls = cls
        super().__init__(people.fio, people.fm, people.parent, people.bd)

class Teacher(People):
    def __init__(self, people, sub="", cls=[]):
        self.sub =sub
        self.cls = cls
        super().__init__(people.fio, people.fm, people.parent, people.bd)



peoples =[
    People({"F": "Иванов", 'I': "Владимир", 'O': "Анатольевич"}, 1),
    People({"F": "Иванова", 'I': "Лидия", 'O': "Михайловна"}, 0),
    People({"F": "Иванов", 'I': "Олег", 'O': "Владимирович"}, 1),
    People({"F": "Иванова", 'I': "Анастасия", 'O': "Владимировна"}, 0),
    People({"F": "Сидоров", 'I': "Игорь", 'O': "Феофанович"}, 1),
    People({"F": "Сидорова", 'I': "Людмила", 'O': "Александровна"}, 0),
    People({"F": "Сидоров", 'I': "Михаил", 'O': "Игоревич"}, 1),
    People({"F": "Петров", 'I': "Марат", 'O': "Тармудзинов"}, 1),
    People({"F": "Петрова", 'I': "Мафият", 'O': "Абдурахмановна"}, 0),
    People({"F": "Петрова", 'I': "Зульфия", 'O': "Маратовна"}, 0),
    People({"F": "Петрова", 'I': "Альма", 'O': "Маратовна"}, 0),
    People({"F": "Петрова", 'I': "Гульчатай", 'O': "Маратовна"}, 0),
    People({"F": "Иванов", 'I': "Владимир", 'O': "Васильевич"}, 1)
]

peoples[2].parent = {'f': peoples[0], 'm': peoples[1]}
peoples[3].parent = {'f': peoples[0], 'm': peoples[1]}
peoples[6].parent = {'f': peoples[4], 'm': peoples[5]}
peoples[9].parent = {'f': peoples[7], 'm': peoples[8]}
peoples[10].parent = {'f': peoples[7], 'm': peoples[8]}
peoples[11].parent = {'f': peoples[7], 'm': peoples[8]}

students = [
    Student(peoples[2], "5A"),
    Student(peoples[3], "1B"),
    Student(peoples[6], "2E"),
    Student(peoples[9], "5A"),
    Student(peoples[10], "1E"),
    Student(peoples[11], "5A")
]

theachers =[
    Teacher(peoples[0], "математика", ["5A", "2E"]),
    Teacher(peoples[1], "математика", ["1B", "1E", "1А"]),
    Teacher(peoples[12], "физкультура", ['1B', '1E', '5A', '2E']),
    Teacher(peoples[8], "ИЗО", ['1B', '1E']),
    Teacher(peoples[5], "литература", ["5A", "2B"]),
]
#1. список классов
cls = list(set([x.cls for x in students]))
#2. список учеников по классам
stud = {i: [j.sFIO() for j in students if j.cls == i] for i in cls}
#3. список всех предметов и учеников
stud_sub = {st.sFIO(): {'class': st.cls, 'theachers': [th.sFIO() for th in theachers if st.cls in th.cls], 'sub': [th.sub for th in theachers if st.cls in th.cls]} for st in students  }
#4. список Учеников с родителями
stud_par = {x.sFIO(): [x.parent['f'].sFIO(), x.parent['m'].sFIO()] for x in students}
#5. список учитилей по классам
teach_cls = {i: [j.sFIO() for j in theachers if i in j.cls] for i in cls }

print(stud_sub)
def print_chois():
    print("Выберите нужное действие")
    print("1. Вывести список учеников")
    print("2. Вывести список учителей")
    print("3. Вывести список классов")
    print("4. Вывести список учеников по классам")
    print("5. Вывести список учителей по классам")
    print("6. Вывести список учеников с родителями")
    print("7. Вывести класс, предметы и учителей конкреного ученика")
    print("8. Вывести учащихся конкретного класса")
    print("9. Вывести учитилей конкретного класса")
    print("10. Вывести родителей конкретного ученика")
    return input(f"{mess} $> ")


def prn_fio_student():
    print('\n'.join(["{}. {}".format(i + 1, x.sFIO()) for i, x in enumerate(students)]))


def prn_fio_teacher():
    print('\n'.join(["{}. {}".format(i + 1, x.sFIO()) for i, x in enumerate(theachers)]))


def prn_class():
    print('\n'.join(sorted(list(set([x.cls for x in students])))))


def prn_stud_class():
    print('\n'.join(['{} \n{}'.format(k, '\n'.join([' {}'.format(v) for v in x])) for k, x in stud.items()]))


def prn_teach_class():
    print('\n'.join(['{} \n{}'.format(k, '\n'.join([' {}'.format(v) for v in x])) for k, x in teach_cls.items()]))


def prn_stud_par():
    print('\n'.join(['{} \n{}'.format(k, '\n'.join(['    {}'.format(v) for v in x])) for k, x in stud_par.items()]))#, '\n'.join([' {}'.format(v) for v in x['sub']])


def prn_stud_sub():
    print('\n'.join(['{} - {}\n предметы:\n{}\n учителя:\n{}'.format(k, x['class'], '\n'.join(['    {}'.format(v) for v in x['sub']]), '\n'.join(['    {}'.format(v) for v in x['theachers']])) for k, x in stud_sub.items()]))


def prn_stud_class_inp():
    prn_class()
    u_inp = input(f"Введите класс буквы в латинском алфавите $> ")
    student = [x.sFIO() for x in students if u_inp == x.cls]
    print(f'В классе {u_inp} ', 'не найдено учеников' if not student else 'учатся: \n{}'.format('\n'.join(student)))


def prn_teach_class_inp():
    prn_class()
    u_inp = input(f"Введите класс буквы в латинском алфавите $> ")
    teachers = [x.sFIO() for x in theachers if u_inp in x.cls]
    print(f'В классе {u_inp} ', 'не найдено учитилей' if not teachers else 'преподают: \n{}'.format('\n'.join(teachers)))

def prn_stud_par_inp():
    prn_fio_student()
    u_inp = input(f"Введите ФИО ученика в русском алфавите $> ")
    student = ['Ученик: {}, отец: {}, мать: {}'.format(x.sFIO(), "нет информации" if not x.parent['f'] else x.parent['f'].sFIO(), "нет информации" if not x.parent['m'] else x.parent['m'].sFIO()) for x in students if u_inp.lower() == x.sFIO().lower()]
    print('не найдено такого ученика' if not student else student[0])

run = [prn_fio_student, prn_fio_teacher, prn_class, prn_stud_class, prn_teach_class,
       prn_stud_par, prn_stud_sub, prn_stud_class_inp, prn_teach_class_inp, prn_stud_par_inp]
lrun = len(run)
uinp = -1
mess = 'Введите цифры от 1 до {} либо "q" для завершения работы'.format(lrun)
uinp = print_chois()
while True:
    if uinp == 'm':
        uinp = print_chois()
    if uinp == 'q' or uinp == 'quit' or uinp == 'exit':
        print('bye-bye')
        break
    try:
        ind = int(uinp)-1
        if ind > lrun-1 or ind < 0:
            uinp = print_chois()
        else:
            run[ind]()
            uinp = input(f"Вернутся в главное меню 'm' выход 'q'  $> ")
    except ValueError:
        uinp = print_chois()


"""
print(cls)
print()
print(stud)
print()
print(stud_sub)
print()
print(stud_par)
print()
print(teach_cls)
print()
print('\n'.join(['{} - {}, отец: {}, мать: {}'.format(x.sFIO(), x.cls, "нет информации" if not x.parent['f'] else x.parent['f'].sFIO(), "нет информации" if not x.parent['m'] else x.parent['m'].sFIO()) for x in students]))
print()
print('\n'.join(['{}, отец: {}, мать: {}'.format(x.sFIO(), "нет информации" if not x.parent['f'] else x.parent['f'].sFIO(), "нет информации" if not x.parent['m'] else x.parent['m'].sFIO()) for x in peoples]))
"""

