__author__ = 'Валерий Сергеевич Коваленко'
# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.
from  math import  sqrt as sq
class Triangle:

    def __init__(self, points=[[1,4], [5,6], [6,2]]):
        self.points = points

    _sides = []

    def sides(self):
        self._sides.clear()
        ln = len(self.points)
        for i in range(ln):
            j = i + 1 if i != ln - 1 else 0
            self._sides.append(sq((self.points[i][0] - self.points[j][0]) ** 2 + (self.points[i][1] - self.points[j][1]) ** 2))

    def perim(self):
        self.sides()
        return sum(self._sides)

    def area(self):
        pp = self.perim() / 2
        return sq(pp*(pp-self._sides[0])*(pp-self._sides[1])*(pp-self._sides[2]))

    def hight(self):
        ar = self.area()
        return 2*ar/self._sides[2]


a = Triangle()
print("Треугольник : периметр - {}, площадь - {}, высота {}".format(round(a.perim(), 2), round(a.area(), 2), round(a.hight(), 2)))



# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.

class Trapeze:

    def __init__(self, points=[[2, 6], [4, 2], [5, 4], [1, 5]]):
        #Сразу расставим точки правильно по часовой стрелке
        #найдем точку лежащую ближе всех к  началу координат по y
        #а затем будем брать самую левую точку последовательно
        self.points = []
        rg = range(len(points))
        y = [y[1] for y in points]
        x = [x[0] for x in points]

        m = min(y)
        i = [i for i, v in enumerate(y) if v == m]
        t = [x[j] for j in rg if j in i]
        m = min(t)
        i = i[t.index(m)]
        self.points.append(points[i])
        x.pop(i), y.pop(i), points.pop(i)

        m = min(x)
        i = [i for i, v in enumerate(x) if v == m]
        t = [y[j] for j in rg if j in i]
        m = min(t)
        i = i[t.index(m)]
        self.points.append(points[i])
        x.pop(i), y.pop(i), points.pop(i)

        m = max(y)
        i = [i for i, v in enumerate(y) if v == m]
        t = [x[j] for j in rg if j in i]
        m = max(t)
        i = i[t.index(m)]
        self.points.append(points[i])
        x.pop(i), y.pop(i), points.pop(i)

        self.points.append(points[0])

    _sides = []
    _diag = []
    _osn = []

    def sides(self):
        self._sides.clear()
        ln = len(self.points)
        for i in range(ln):
            j = i + 1 if i != ln - 1 else 0
            self._sides.append(sq((self.points[i][0] - self.points[j][0]) ** 2 + (self.points[i][1] - self.points[j][1]) ** 2))

    def diag(self):
        self._diag.clear()
        self._diag.append(sq((self.points[0][0] - self.points[2][0]) ** 2 + (self.points[0][1] - self.points[2][1]) ** 2))
        self._diag.append(sq((self.points[1][0] - self.points[3][0]) ** 2 + (self.points[1][1] - self.points[3][1]) ** 2))

    def _cos(self, sides):
        return round((sides[1]**2 + sides[2]**2 - sides[0]**2)/(2*sides[1]*sides[2]), 5)

    def _cugol(self):
        cs = []
        cs.append(self._cos([self._sides[0], self._sides[1], self._diag[0]]))
        cs.append(self._cos([self._sides[2], self._sides[3], self._diag[0]]))
        cs.append(self._cos([self._sides[3], self._sides[0], self._diag[1]]))
        cs.append(self._cos([self._sides[1], self._sides[2], self._diag[1]]))
        return cs

    def is_trap(self):
        self.sides()
        self.diag()
        #находим косинусы углов диагоналей для выявления паралельности
        cs = self._cugol()

        if cs[0] == cs[1] or cs[1] == cs[2]:
            self._osn = [1, 3] if cs[0] == cs[1] else [0, 2]
            if self._diag[0] == self._diag[1]:
                #print("Это трапеция равнобочная")
                return True
            else:
                #print("Эта трапеция НЕ равнобочная")
                return False
        else:
            #print("Это НЕ трапеция")
            return False

    def perim(self):
        self.sides()
        return round(sum(self._sides), 2)

    def get_sides(self):
        self.sides()
        return [round(x, 2) for x in self._sides]

    def area(self):
        if self.is_trap():
            return round(((self._sides[self._osn[0]] + self._sides[self._osn[1]])/2)*sq(self._sides[self._osn[0]+1]**2 - ((self._sides[self._osn[0]] - self._sides[self._osn[1]])**2)/4), 2)
        else:
            return False



b = Trapeze([[2, 4], [6, 1], [5, 4], [1, 1]])
b.points[0] = [0, 1]
print("Четырех угольник: периметр - {}, стороны - {}, ".format(b.perim(), b.get_sides()), "площадь равнобедренной трапеции - {}".format(b.area()) if b.is_trap() else "данный четырехугольник не является равнобедренной трапецией ")
