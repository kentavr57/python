__author__ = 'Валерий Сергеевич Коваленко'
"""
Очень странное задание для курса на котором вообще базы данных не изучались, но на этом странности не заканчиваются
ЗАчем давать такое задание в котором смысла использовать классы нет априори? - я не использовал
Зачем хранить JSON файл на диске если мы уже работаем с базой данных? - я не стал хранить а просто создал таблицу в базе.
Зачем обрабатывать XML файлы если мы все получаем по JSON? - я не обрабатывал XML файлы.
Теперь о реализации:
Конфиг хранится в файле config.ini
[API]
# Свой ключ "вытащить" со страницы отсюда: https://home.openweathermap.org/api_keys
key = ccd3a7fd4724296c01af0e2af2d711f1
[DB]
# Данные для подключения к базе данных
host= localhost
# база с которой мы хотим работать
database= wheather1  
user= root
password= 123456
#Дополнительно если нужно создать дб
serverbd = mysql

Логика проста пытаемся подключииться к базе если нет, то пытаемся подключиться к серверу и создать базу если опять
постигла неудача коннектимся к файлу database.db с помощью sqlite.
Если мы хотим всегда работать с локальным файлом бд, то из конфига удаляем секцию [DB]
Если база пустая создаем 2 таблицы
city` 
    `id` id города
    `name` Имя города 
    `cid` Двух буквенное обозначение страны
    
`wheather`
    `id` идентификатор уникальный по таблице
    `tid` id города
    `wid` id погоды
    `date` дата без времени
    `tp` температура
    `pic` имя картинки погоды ( по логике ее нужно вынести в отдельную таблицу, но я не стал)

далее если первая таблица пуста загружаем, разархивируем json и распихиваем города по таблице
меню:
ГЛАВНОЕ МЕНЮ
1. Показать регионы
2. Поискать страны (выборка всех городов страны)
3. Поискать города

1. Ищем регионы и можем вывести в подменю температуру по отдельному региону или по всем (8)
2. По двух буквенному обозначению страны выводим список всех городов в стране , можем посмотреть температуру в выбраном городе или по всем городам
3. Поиск города по совпадению части города либо посик по городу и стране через /

Если температура для города уже указана, то обновляем если нет то заносим .. и тут каждый раз тянем JSON  с сервера, что не есть хорошо, зато актуально.
в теории можно сделать ограницение по частоте запросов , а в остальных случаях брать из базы не таская JSON - но я не стал делать )))

Если скрипт вызывается с параметрами то формируется отдача в поток  JSON 

про SQL lite не знал, сделал на номальном мускуле 
инструкция по установке https://uploads.hb.cldmail.ru/asset/1106261/attachment/da57490e4bbdf074ca845edc52865a3a.mp4

"""
from gzip import decompress
from mysql.connector import connect
from configparser import ConfigParser
import json
import requests
import datetime
import sys
import sqlite3

def tru_exit(mess, conn = False, mess2 = ""):
    if conn:
        conn.close()
    if is_prn:
        print(mess)
        input("Нажмите любую клавишу для завершения")
    else:
        print("!Error: db", mess2)
    raise SystemExit

def conf_pars():
    config = ConfigParser()
    global is_mySQL
    try:
        config.read('config.ini')
        appid = config['API']['key']
        if not appid: tru_exit("Ключ APPID должен быть указан в файле config.ini")
        try:
            conf = config['DB']
            return appid, config['DB']
        except:
            is_mySQL = False
            return appid, connect_lsql()
    except:
        tru_exit("Проблеммы с файлом config.ini проверьте конфигурацию", conn=False)

def creat_db(conn, config):
    cursor = conn.cursor()
    cursor.execute(f"CREATE SCHEMA `{config['database']}` ;")
    cursor.close()
    if is_prn: print(f"... создали базу {config['database']}")
    conn = connect_db(config)
    return conn


def creat_tables(conn, flag):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `city` (`id` INT NOT NULL ,`name` VARCHAR(255) NOT NULL, " \
                   "`cid` VARCHAR(3) NOT NULL , PRIMARY KEY (`id`));")
    #print("... создали таблицу 'city'")
    cursor = conn.cursor()
    quer = "CREATE TABLE IF NOT EXISTS `wheather` (`id` INT NOT NULL AUTO_INCREMENT, " \
           "`tid` INT NOT NULL, `wid` INT NOT NULL,`date` DATETIME NOT NULL, " \
           "`tp` FLOAT NULL, `pic` VARCHAR(5), PRIMARY KEY (`id`));" if flag else "CREATE TABLE IF NOT EXISTS `wheather` " \
                                                                                  "(`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , " \
           "`tid` INT NOT NULL, `wid` INT NOT NULL,`date` DATETIME NOT NULL, " \
           "`tp` FLOAT NULL, `pic` VARCHAR(5));"
    cursor.execute(quer)
    #print("... создали таблицу 'wheather'")
    conn.commit()
    cursor.close()


def connect_lsql():
    global is_mySQL
    conn = sqlite3.connect("database.db")
    creat_tables(conn, False)
    is_mySQL = False
    return conn

def connect_db(config, serv = False):
    try:
        bd = config['serverbd'] if serv else config['database']
        conn = connect(host=config['host'],
                                       database = bd,
                                       user = config['user'],
                                       password = config['password'])
        if conn.is_connected():
            if(serv):
                if is_prn: print(f"...начинаем создание новой базы {config['database']}")
                return creat_db(conn, config)
            else:
                creat_tables(conn, True)
                if is_prn: print(f"...успешно соеденились с базой данных {config['database']}")
                return conn
        else:
            tru_exit(f"!Не удалось подключиться к базе данных", conn)
    except Exception as e:
        if is_prn:
            if not serv:
                ans = input("!Не удалось подключиться к базе данных, попробовать подключиться к серверу и создать базу? y/n")
                if ans.lower() == 'y':
                    return connect_db(config, True)
                else:
                    #tru_exit(f"!Не удалось подключиться к базе данных, проверьте настройки config.ini.\nОшибка: {e}")
                    return connect_lsql()
            else:
               #tru_exit(f"!Не удалось подключиться к базе данных, проверьте настройки config.ini.\nОшибка: {e}")
               print("...подключение к серверу не удалось, проверьте настройки config.ini. ")
               print("...работаем с локальной базой данных sqLite")
               return connect_lsql()
        else:
            #tru_exit(f"!Не удалось подключиться к базе данных, проверьте настройки config.ini.\nОшибка: {e}", false, e)
            return connect_lsql()


def get_json(par):
    try:
        rg = 20  # The limit of locations is 20.1
        lpar = len(par)
        if lpar > rg:
            rez = []
            l = lpar // rg
            for i in range(l):
                arr = requests.get(
                    f'http://api.openweathermap.org/data/2.5/group?id={",".join([str(x) for x in par[i * rg:(i + 1) * rg]])}&units=metric&appid={appid}').json()[
                    'list']
                rez += [[x["id"], x["name"], x["sys"]["country"], x["main"]["temp"], x["weather"][0]["icon"], x["weather"][0]["id"]] for x in
                        arr]
            if len(par[l * rg:]) > 0:
                arr = requests.get(
                    f'http://api.openweathermap.org/data/2.5/group?id={",".join([str(x) for x in par[l * rg:]])}&units=metric&appid={appid}').json()[
                    'list']
                rez += [[x["id"], x["name"], x["sys"]["country"], x["main"]["temp"], x["weather"][0]["icon"], x["weather"][0]["id"]] for x in
                        arr]
            return rez
        else:
            arr = requests.get(
                f'http://api.openweathermap.org/data/2.5/group?id={",".join([str(x) for x in par])}&units=metric&appid={appid}').json()[
                'list']
            return [[x["id"], x["name"], x["sys"]["country"], x["main"]["temp"], x["weather"][0]["icon"], x["weather"][0]["id"]] for x in arr]
    except Exception as e:
        tru_exit(f"!Не удалось получить файл. Ошибка: {e}", conn, e)


def get_country():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM city LIMIT 1;")
    if not cursor.fetchone():
        if is_prn: print("...не обнаружено городов в базе, будем загружать")
        try:
            arr = json.loads(decompress(requests.get('http://bulk.openweathermap.org/sample/city.list.json.gz').content))
        except Exception as e:
            tru_exit(f"!Не удалось получить файл с городами. Ошибка: {e}", conn, e)
        city = [(x['id'], x['name'], x['country'] if x['country'] else 'ReG') for x in arr]
        # Падает мой скуль сервер по этому грузим частями по 200 строчек
        rg = 200
        x = len(city) // rg
        for i in range(x):
            quer = "INSERT INTO city(id,name,cid) VALUES(%s,%s,%s);" if is_mySQL else "INSERT INTO city(id,name,cid) VALUES(?,?,?);"
            cursor.executemany(quer, city[i * rg:(i + 1) * rg])
            conn.commit()
        if len(city[x * rg:]) > 0:
            cursor.executemany(quer, city[x * rg:])
        conn.commit()
        cursor.close()


def show_reg(par=''):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM city where cid = 'ReG';")
    reg = cursor.fetchall()
    cursor.close()
    menu = [x[1] for x in reg]
    par = [x[0] for x in reg]
    run =[prn_wd]
    print_chois('Выбор региона', menu, run, par)


def put_wd(data, par):
    arr = get_json(par)
    ins_arr = [(x[0], x[5], data, x[3], x[4]) for x in arr]
    ins = []
    cursor = conn.cursor()
    for x in ins_arr:
        tid = x[0]
        try:
            quer = "SELECT id FROM wheather WHERE`tid` = %s AND `date` = %s;" if is_mySQL else "SELECT id FROM wheather WHERE`tid` = ? AND `date` = ?;"
            cursor.execute(quer,(tid, data))
        except:
            pass  # Я не знаю что тут и в похожих местах за исключение видимо какойто глюк mysql.connector  но тем не менее все работает
        rez = cursor.fetchone()
        if rez:
            try:
                quer = "UPDATE `wheather` SET `tp`=%s  WHERE (`id` = %s);" if is_mySQL else "UPDATE `wheather` SET `tp`=?  WHERE (`id` = ?);"
                cursor.execute(quer, (x[3], rez[0]))
                conn.commit()
            except:
                pass
        else:
            ins.append(x)
    try:
        cursor.close()
    except:
        pass
    if ins:
        cursor = conn.cursor()
        quer = "INSERT INTO  wheather (`tid`, `wid`, `date`, `tp`, `pic`) VALUES (%s,%s,%s,%s,%s);" if is_mySQL else "INSERT INTO  wheather (`tid`, `wid`, `date`, `tp`, `pic`) VALUES (?,?,?,?,?);"
        cursor.executemany(quer, ins)
        conn.commit()
        cursor.close()
    return [x[:5] for x in arr]


def prn_wd( par=''):
    print("Получение температуры", par[1])
    data = datetime.date.today()
    if type(par[0]) != list:
        par[0]=[par[0]]
    arr = put_wd(data, par[0])
    [print('{:<25} : {}°C'.format('{} ({})'.format(x[1], '--' if x[2] == 'ReG' or x[2] == '' else x[2]), x[3])) for x in arr]
    input("Нажмите 'ENTER' для возврата в меню")

def search_country(par=''):
    print("Поиск страны")
    while True:
        in_coun = input("Введите двух буквенное обозначение страны $>")
        if len(in_coun) > 1:
            in_coun = f'%{in_coun}%'
            break
    cursor = conn.cursor()
    quer = "SELECT * FROM city WHERE  cid LIKE %s" if is_mySQL else "SELECT * FROM city WHERE  cid LIKE ?"
    cursor.execute(quer,(in_coun,))
    reg = cursor.fetchall()
    cursor.close()
    menu = [x[1] for x in reg]
    par = [x[0] for x in reg]
    run = [prn_wd]
    print_chois('Выбор города', menu, run, par)

def search_city(par=''):
    print("Поиск города")
    in_city = input("Введите название города либо часть названия (через / можно ввести двух буквенное обозначение страны для уточнения поиска) $>")
    in_city = in_city.split('/')
    if len(in_city) > 1:
        quer = "SELECT * FROM city WHERE name LIKE %s AND cid LIKE %s" if is_mySQL else "SELECT * FROM city WHERE name LIKE ? AND cid LIKE ?"
        in_city = (f'%{in_city[0].strip()}%', f'%{in_city[1].strip()}%')
    else:
        quer = "SELECT * FROM city WHERE name LIKE %s" if is_mySQL else "SELECT * FROM city WHERE name LIKE ?"
        in_city = (f'%{in_city[0].strip()}%',)
    cursor = conn.cursor()
    cursor.execute(quer, in_city)
    reg = cursor.fetchall()
    cursor.close()
    menu = ['{} ({})'.format(x[1], x[2]) for x in reg]
    par = [x[0] for x in reg]
    if len(par) == 1:
        prn_wd([par[0], menu[0]])
    else:
        run = [prn_wd]
        print_chois('Выбор города', menu, run, par)


def print_chois(ms, menu, run, par=''):
    while True:
        print()
        print(ms)
        lrun = len(menu)
        if par:
            mess = 'Введите цифры от 0 до {} либо "m" для перехода в предыдущее меню'.format(lrun)
            print("0. По всем найденным")
        else:
            mess = 'Введите цифры от 1 до {} либо "q" для завершения работы'.format(lrun)

        [print("{}. {}".format(i+1, v)) for i, v in enumerate(menu)]
        uinp = input(f"{mess} $> ")
        if uinp == 'q' or uinp == 'quit' or uinp == 'exit':
            print('bye-bye')
            break
        if uinp == 'm': break
        try:
            ind = int(uinp)-1
            if ind == -1 and par:
                run[0]([par, 'По всем найденным'])
            elif not(ind > lrun-1 or ind < 0):
                if par:
                    run[0]([par[ind], menu[ind]])
                else:
                    run[ind]()
        except:
            pass

def export_arr(par):
    data = datetime.date.today()

    if par:
        quer = "SELECT * FROM city WHERE name LIKE %s" if is_mySQL else "SELECT * FROM city WHERE name LIKE ?"
        in_city = (f'%{par.strip()}%',)
        cursor = conn.cursor()
        cursor.execute(quer, in_city)
        par = cursor.fetchall()
        cursor.close()
        par = [x[0] for x in par]
        arr = []
        i = []
        cursor = conn.cursor()
        for tid in par:
            try:
                quer = "SELECT * FROM wheather as A LEFT JOIN city as B ON (A.tid = B.id) WHERE A.`tid` = %s AND A.`date` = %s" if is_mySQL else "SELECT * FROM wheather as A LEFT JOIN city as B ON (A.tid = B.id) WHERE A.`tid` = ? AND A.`date` = ?"
                cursor.execute(quer, (tid, data))
            except:
                pass # Я не знаю что тут и в похожих местах за исключение видимо какойто глюк mysql.connector  но тем не менее все работает
            rez = cursor.fetchone()
            if rez:
                arr.append([rez[1], rez[7], rez[8], rez[4], rez[5]])
            else:
                i.append(tid)
        try:
            cursor.close()
        except:
            pass
        if i:
            arr += put_wd( data, i)
        arr = [{'id': x[0], 'name': x[1], 'country': x[2], 'temp': x[3], 'pic': x[4]} for x in arr]
    else:
        try:
            cursor = conn.cursor()
            quer = "SELECT * FROM wheather as A LEFT JOIN city as B ON (A.tid = B.id) WHERE  A.`date` = %s;" if is_mySQL else "SELECT * FROM wheather as A LEFT JOIN city as B ON (A.tid = B.id) WHERE  A.`date` = ?;"
            cursor.execute(quer, (data,))
            rez = cursor.fetchall()
            if rez:
                arr = [{'id': x[1], 'name': x[7], 'country': x[8], 'temp':x[4], 'pic': x[5]} for x in rez]
            cursor.close()
        except :
            pass  # Я не знаю что тут и в похожих местах за исключение видимо какойто глюк mysql.connector  но тем не менее все работает
    return arr


def export_json(city = ''):
    arr = export_arr(city)
    arr = json.dumps(arr)
    print(arr)


#Начало работы
is_prn = True if len(sys.argv) == 1 else False
is_mySQL = True
appid, conf = conf_pars()
conn = connect_db(conf) if is_mySQL else conf
get_country()

if is_prn:
    mmenu = [
        "Показать регионы",
        "Поискать страны (выборка всех городов страны)",
        "Поискать города"
    ]
    print_chois('ГЛАВНОЕ МЕНЮ', mmenu, [show_reg, search_country, search_city])
else:
    city ='' if sys.argv[1] == None else sys.argv[1].strip()
    export_json(city)
conn.close()


