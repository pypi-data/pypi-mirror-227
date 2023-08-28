def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


class Number:
    def __init__(self, num: int, den: int = 1):
        self.num = num
        self.den = den
        self.reduce()

    def opposite(self):
        return Number(self.num * -1, self.den)

    def inverse(self):
        return Number(self.den, self.num)

    def __eq__(self, number):
        return self.num == number.num and self.den == number.den

    def __add__(self, number):
        result = Number(self.num * number.den + number.num *
                        self.den, self.den * number.den)
        result.reduce()
        return result

    def __sub__(self, number):
        return self + number.opposite()

    def __mul__(self, number):
        result = Number(self.num * number.num, self.den * number.den)
        result.reduce()
        return result

    def __truediv__(self, number):
        return self * number.inverse()

    def __floor__(self):
        return Number(self.num // self.den, 1)

    def __ceil__(self):
        return self.__floor__() + Number(1, 1)

    def reduce(self):
        div = gcd(self.num, self.den)
        self.num = self.num // div
        self.den = self.den // div

    def __str__(self):
        return f"{self.num}" if self.den == 1 else f"{self.num}/{self.den}"

    def _ipython_display_(self):
        print(self)

    def to_float(self):
        return self.num / self.den

    @staticmethod
    def parse(decimal: str):
        coef = -1 if decimal.startswith("-") else 1
        splits = decimal.removeprefix("-").split(".")
        den = 1 if len(splits) == 1 else 10 ** len(splits[1])
        return Number(coef * int("".join(splits)), den)
