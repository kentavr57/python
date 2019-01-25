#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""
__author__ = 'Валерий Сергеевич Коваленко'
"""
!!!!!!!!!!  ВАЖНО  !!!!!!!!!!!!
Немного про карточки, действительно 27 клеток, и действительно 15 из них должны быть активными, но оба примера 
приведенные в задании не верны, т.к. в карточках есть столбцы и эти столбцы отвечают за десятки в первом столбце могут 
распологаться цифры от 1 до 9 ти, во втором от  10 до 19 и т.д. за исключением последнего в который добавляется цифра 90
отсюда следует что из каждого десятка в карточке не может быть больше 3х цифр , меньше может , может вообще не быть, но 
больше быть не может, логично что и в каждой строке может быть только одна цифра из одного десятка,
а у вас в каждой карточке ошибка в примерах. 
https://yandex.ru/images/search?text=%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B8%20%D0%BB%D0%BE%D1%82%D0%BE%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8&lr=213
"""
from  random import randint as ri

class Pole(list):
    def apd(self,zn):
        if zn > 0:
            self.append([zn, str(zn)])
        else:
            self.append([0, ''])

    def get_prn(self):
        return [x[1] for x in self]

    def get_zn(self):
        return [x[0] for x in self]

    def frm_slice(self,kolvo):
        ln = len(self)
        rd = ln // kolvo
        tmp = ''
        for i in range(rd):
            tmp += ''.join(['{:<3}'.format(x[1]) for x in self[i*kolvo:(i+1)*kolvo]])
            tmp += '\n'
        return tmp

    def vich(self, el):
        i = self.findx(el)
        if i == None:
            return False
        else:
            self[i][1] = '-'
            return True

    def findx(self, el):
        try:
            return [x[0] for x in self].index(el)
        except:
            return None


class Cart:
    def __init__(self, name="user_name", cname='cart_name'):
        self.cart = Pole() #карточка
        self.numb = []
        self.name = name
        self.cname = cname
        self.gen_cart()
        self._win = False

    def __str__(self):
        return self.prn_cart()

    def gen_cart(self):
        self.numb = []
        for i in range(3):
            des = []  #десятки
            line =[]  #линии
            for j in range(5):
                while True:
                    r = ri(1, 90)
                    rd = 8 if r == 90 else r // 10
                    if r not in self.numb and rd not in des:
                        line.append(r)
                        self.numb.append(r)
                        des.append(rd)
                        break
            for n in range(9):
                if n in des:
                    self.cart.apd(line[des.index(n)])
                else:
                    self.cart.apd(0)

    def ofr_cart(func):
        def decorated(*args, **kwargs):
            n = len(args[0].cname) + 2
            s = (27 - n) // 2
            tmp = "{} {} {}\n".format('-' * s, args[0].cname, '-' * (27 - s - n))
            tmp += func(*args, **kwargs)
            tmp += '-' * 27
            return tmp + '\n'
        return decorated

    @ofr_cart
    def prn_cart(self):
        return self.cart.frm_slice(9)

    def die(self, nomer, fl):
        fl = 'есть номер' if fl else 'нет номера'
        print(f'!!!!  Вы ({self.name}) проиграли так как в Вашей карточке "{self.cname}" {fl}: {nomer}')
        input("Для завершения нажмите любую клавишу")
        raise SystemExit(0)

    def win(self):
        if self._win:
            print(f'!!!!  Победил {self.name} на карточке "{self.cname}"')
            print(self.prn_cart())

    def vich(self, nomer):
        if nomer in self.numb:
            del (self.numb[self.numb.index(nomer)])
            self.cart.vich(nomer)
        if len(self.numb):
            return 1
        else:
            self._win = True
            return 0

    def xod(self, nomer, fl):
        if fl:
            uin = input("Зачеркнуть цифру? (y / n)")
            if uin.lower() == 'y':
                if nomer in self.numb:
                    return self.vich(nomer)
                else:
                    return self.die(nomer, False)
            else:
                if nomer in self.numb:
                    return self.die(nomer, True)
                else:
                    return 1
        else:
            if nomer in self.numb:
                return self.vich(nomer)
            else:
                return 1

    def __call__(self, *args, **kwargs):
        return self.xod(args[0], args[1])


class IterObj:
    def __init__(self, numb):
        self.numb = numb
        self.vich = []

    def __next__(self):
        if len(self.numb):
            while True:
                r = ri(1, 90)
                if r not in self.vich:
                    self.vich.append(r)
                    if r in self.numb:
                        del(self.numb[self.numb.index(r)])
                    break
            return r
        else:
            raise StopIteration


class Iter:
    def __init__(self, numb):
        self.numb = list(set(numb))

    def __iter__(self):
        return IterObj(self.numb)

print('*'*31)
print('*'*10, "Игра ЛОТО", '*'*10)
print('*'*31)
print()
#создадим массив игроков их может быть больше двух либо играть можно на нескольких карточках
#Массив каждого игрока содержит класс игрока, флаг живого человека, и флаг победы ( 0 - закрыл все цифры, 1 -еще не все)

def form_igrocks():
    igroks = []
    kc= input("Введите сколько карточек будет на руках у каждого игрока от одной до бесконечности :)")
    try:
        kc =int(kc)
    except:
        kc = 1
    kc = 1 if kc <= 0 else kc
    ai = input("Введите сколько AI будут учавствовать в игре от нуля и больше :)")
    try:
        ai =int(ai)
    except:
        ai = 1
    ai = 1 if ai < 0 else ai
    hi = input("Введите сколько игроков будут учавствовать в игре от нуля и больше :)")
    try:
        hi = int(hi)
    except:
        hi = 1
    hi = 1 if hi < 0 else hi
    if ai + hi == 0:
        print("Судя по всему никто играть не будет")
        input("Для завершения нажмите любую клавишу")
        raise SystemExit(0)
    else:
        print(f"Играть будут: {ai} компьютер(а/ов) и {hi} игрок(a/ов) (по системе хот сит) на {kc} карточке(ах) у каждого")
    for i in range(ai):
        if ai == 1:
            name = "Компьютер"
        else:
            name = "Компьютер"+str(i+1)
        if kc == 1:
            igroks.append([Cart(name, "Карточка компьютера"+str(i+1)), False, 1])
        else:
            for j in range(kc):
                igroks.append([Cart(name, "Карточка № {} компьютера{}".format(j+1, i+1)), False, 1])
    for i in range(hi):
        name = input(f'Введите имя {i+1} игрока')
        name = name.title()
        if kc == 1:
            igroks.append([Cart(name, "{} карточка".format(name[:-1]+'ина')), True, 1])
        else:
            for j in range(kc):
                igroks.append([Cart(name, "{} карточка № {}".format(name[:-1] + 'ина', j+1)), True, 1])
    return igroks


#Для проверки программы на завершенность расскоментируйте первый массив, копьютер сыграет сам с собой на 4х карточках.
#Второй массив позволит побыстрее протестировать игру, т.к. против вас будут играть 4ре компьютера

igroks = form_igrocks() #закоментируйте если не хотите при тесте формировать игроков, а берете игроков из нижележащих массивов
#igroks =[[Cart("Компьютер", "Карточка № 1"), False, 1],[Cart("Компьютер", "Карточка № 2"), False, 1],[Cart("Компьютер", "Карточка № 3"), False, 1],[Cart("Компьютер", "Карточка № 4"), False, 1]]
#igroks =[[Cart("Компьютер", "Карточка компьютера"), False, 1],[Cart("Компьютер2", "Карточка компьютера2"), False, 1],[Cart("Компьютер3", "Карточка компьютера3"), False, 1],[Cart("Компьютер4", "Карточка компьютера4"), False, 1],[Cart("Вы", "Ваша карточка"), True, 1]]
#igroks =[[Cart("Компьютер", "Карточка компьютера"), False, 1],[Cart("Вы", "Ваша карточка"), True, 1]]


def igra(igroks):
    lni = len(igroks)
    numb = []
    for igr in igroks:
        numb += igr[0].numb
    it = Iter(numb)
    for i, boch in enumerate(it):  #достаем боченки
        print('*'*10, "Ход номер: ", i+1, '*'*30)
        print(f"Новый бочонок: {boch} (осталось {89 - i} бочёнка в мешочке)")
        fl = 0
        for igr in igroks:
            print(igr[0])
            igr[2] = igr[0](boch, igr[1])
            fl += igr[2]
        if fl != lni:
            if lni-fl > 1:
                print(f'!!!!  Ничья , такое случается редко но случается :)')
                for igr in igroks:
                    igr[0].win()
            else:
                for igr in igroks:
                    igr[0].win()
            break
        print()
        print()

igra(igroks)

input("Для завершения нажмите любую клавишу")
