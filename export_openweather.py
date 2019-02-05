__author__ = 'Валерий Сергеевич Коваленко'
""" OpenWeatherMap (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]
    
При выгрузке в html можно по коду погоды (weather.id) подтянуть 
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions

Экспорт происходит в файл filename.

Опционально можно задать в командной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
загружаются данные с сайта


"""

import csv
import json
from subprocess import Popen, PIPE
import sys
import argparse

def get_json():
    try:
        out, err = Popen(f"python openweather.py {ns.city}", shell=True, stdout=PIPE).communicate()
        out = str(out, 'utf-8')  # , 'ignore'
        #print(out)
        if '!Error:' in out:
            print("Ошибка загрузки данных")
            raise SystemExit
        else:
            try:
                return json.loads(out)
            except Exception as e:
                print('Ошибка десериализации данных', e)
                raise SystemExit
    except Exception as e:
        print("Не смог получить данные",e)


def put_json():
    arr = get_json()
    print(arr)
    try:
        with open(ns.json+".json", "w") as f:
            json.dump(arr, f)
        print(f"Создан файл JSON, {ns.json}.json ")
    except Exception as e:
        print('Ошибка записи JSON в файл', e)
        raise SystemExit



def put_csv():
    arr = get_json()
    title = [[i for i in arr[0]]]
    arr = [[v for k, v in x.items()] for x in arr]
    arr = title + arr
    # не знаю я как заставить пайтон работать с албанским по этому извращаюсь
    #'charmap' codec can't encode character '\u0101' in position 0: character maps to <undefined>
    # начало извращений
    arr = json.dumps(arr)
    arr = arr.replace('[[','')
    arr = arr.replace(']]', '')
    arr = arr.replace('"', '')
    line = arr.split('], [')
    arr = [x.split(',') for x in line]
    print(arr)
    #конец извращений
    try:
        with open(ns.csv+".csv", "w") as f:
            wr = csv.writer(f, delimiter=',')
            for line in arr:
                wr.writerow(line)
        print(f"Создан файл CSV, {ns.csv}.csv ")
    except Exception as e:
        print('Ошибка записи CSV в файл', e)
        raise SystemExit


def put_html():
    #оформлять штмл не стал - если нужно то дизайнер стили в шаблон подсунет
    arr = get_json()
    thm_line = '<tr><td>{}</td><td><img src="http://openweathermap.org/images/flags/{}.png" /></td><td>{}&deg;C</td><td><img src="http://openweathermap.org/img/w/{}.png" /></td></tr>'
    thm_line = ''.join([thm_line.format(x['name'],x['country'].lower(),x['temp'],x['pic']) for x in arr])
    try:
        with open("shablon.thm") as f:
            sbhtml = f.read().strip()
        sbhtml = sbhtml.replace('{%TABLE%}',thm_line)
        try:
            with open(ns.html+'.html', 'w') as f:
                f.writelines(sbhtml)
            print(f"Создан файл HTML, {ns.html}.html ")
        except Exception as e:
            print('Ошибка записи HTML в файл', e)
            raise SystemExit
    except Exception as e:
        print('Ошибка открытия шаблона HTML', e)
        raise SystemExit


parser = argparse.ArgumentParser()
parser.add_argument ('--json', nargs='?')
parser.add_argument ('--csv', nargs='?')
parser.add_argument ('--html', nargs='?')
parser.add_argument ('city', nargs='?')
ns = parser.parse_args(sys.argv[1:])
#print(ns)
if ns.json != None:
    put_json()
elif ns.csv != None:
    put_csv()
elif ns.html != None:
    put_html()
else:
    print('Формат вызова программы :'
          '\nexport_openweather.py --csv filename [<город>]'
          '\nexport_openweather.py --json filename [<город>]'
          '\nexport_openweather.py --html filename [<город>]')



