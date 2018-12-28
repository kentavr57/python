
__author__ = 'Валерий Сергеевич Коваленко'

# Задача-1: Дано произвольное целое число, вывести самую большую цифру этого числа.
# Например, дается x = 58375.
# Нужно вывести максимальную цифру в данном числе, т.е. 8.
# Подразумевается, что мы не знаем это число заранее.
# Число приходит в виде целого беззнакового.
# Подсказки:
# * постарайтесь решить задачу с применением арифметики и цикла while;
# * при желании и понимании решите задачу с применением цикла for.

#user_input = int(input('Введите число: '))
#max = user_input%10
#while user_input != 0:
#    per = user_input%10
#    if per > max:
#        max = per
#    user_input = user_input // 10
#print ('Наибольшая цифра: ',max)

user_input = input('Введите число: ')
max = int(user_input[0])
for per in user_input:
    per = int(per)
    if per > max:
       max = per
print ('Наибольшая цифра: ',max)


# Задача-2: Исходные значения двух переменных запросить у пользователя.
# Поменять значения переменных местами. Вывести новые значения на экран.
# Решите задачу, используя только две переменные.
# Подсказки:
# * постарайтесь сделать решение через действия над числами;
# * при желании и понимании воспользуйтесь синтаксисом кортежей Python.

#user_input_a = int(input('Введите число a: '))
#user_input_b = int(input('Введите число b: '))
#user_input_b *= user_input_a
#user_input_a = user_input_b/user_input_a
#user_input_b = user_input_b/user_input_a
#print("a = ",int(user_input_a),"b = ", int(user_input_b))

user_input_a = input('Введите число a: ')
user_input_b = input('Введите число b: ')
user_input_a , user_input_b = user_input_b , user_input_a
print("a = ",int(user_input_a),"b = ", int(user_input_b))

# Задача-3: Напишите программу, вычисляющую корни квадратного уравнения вида
# ax² + bx + c = 0.
# Коэффициенты уравнения вводятся пользователем.
# Для вычисления квадратного корня воспользуйтесь функцией sqrt() модуля math:
# import math
# math.sqrt(4) - вычисляет корень числа 4

import math
print('Решение квадратного уравнения вида ax**2 + bx + c = 0')
koef_a = 0
while koef_a == 0:
    koef_a = int(input('Введите коэффициент a, а > 0: '))
koef_b = int(input('Введите коэффициент b: '))
koef_c = int(input('Введите коэффициент c: '))
disc = koef_b * koef_b-4 * koef_a * koef_c
print ('Дискриминант D=',disc)
if disc == 0:
    koren = (math.sqrt(disc)-koef_b) / (2 * koef_a)
    print('Уравнение имеет одно решение : ',koren)
elif disc > 0:
    koren_1 = (math.sqrt(disc)-koef_b) / (2 * koef_a)
    koren_2 = (0 - math.sqrt(disc)-koef_b) / (2 * koef_a)
    print('Уравнение имеет два решения : ', koren_1, ' и ',koren_2)
else:
    print('Уравнение не имеет решений : ')