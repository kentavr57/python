# Задание-1:
# Напишите функцию, округляющую полученное произвольное десятичное число
# до кол-ва знаков (кол-во знаков передается вторым аргументом).
# Округление должно происходить по математическим правилам (0.6 --> 1, 0.4 --> 0).
# Для решения задачи не используйте встроенные функции и функции из модуля math.
print(">>> Функция, округления")
def my_round(number, ndigits):
    drob = str(number).split(".")
    per = int(drob[1][ndigits-1])
    if per == 9:
        nd = 2
        while (ndigits - nd) >= 0:
            per = int(drob[1][ndigits - nd])
            if per == 9:
                nd += 1
            else:
                break
        if nd > ndigits:
            number = int(drob[0])+1
        else:
            number = float(drob[0] + "." + drob[1][0:ndigits - nd] + str(per+1))
    elif per >=5:
        number = float(drob[0]+"."+drob[1][0:ndigits-1]+str(per+1))
    else:
        number = float(drob[0] + "." + drob[1][0:ndigits - 1] + str(per))

    return number


print(my_round(2.1234567, 5))
print(my_round(2.1999967, 5))
print(my_round(2.9999967, 5))
print(my_round(2.1111167, 3))


print(">>> Функция, округления из разбора")
def my_round2(number, ndigits):
    big_num = number * (10 ** (ndigits+1))
    if big_num % 10 >= 5:
        big_num += 10
    big_num = int(big_num/10) / (10 ** ndigits)
    return  big_num

print(my_round2(2.1234567, 5))
print(my_round2(2.1999967, 5))
print(my_round2(2.9999967, 5))
print(my_round2(2.1111167, 3))



# Задание-2:
# Дан шестизначный номер билета. Определить, является ли билет счастливым.
# Решение реализовать в виде функции.
# Билет считается счастливым, если сумма его первых и последних цифр равны.
# !!!P.S.: функция не должна НИЧЕГО print'ить
print(">>> Функция, счачтливый билетик")
def summ_numb(numb):
    summ = 0
    while numb != 0:
        summ += numb%10
        numb = numb // 10
    return summ


def lucky_ticket(ticket_number):
    if summ_numb(ticket_number//1000) == summ_numb(ticket_number%1000):
        return "lucky"
    else:
        return "not lucky"


print(lucky_ticket(123006))
print(lucky_ticket(12321))
print(lucky_ticket(436751))
