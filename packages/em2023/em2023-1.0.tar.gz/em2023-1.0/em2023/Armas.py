from random import randint

class Misil:
    def __init__(self, diametro=10):
        self.diametro = diametro
        self.potencia = diametro * randint(1, 10)
    def __str__(self):
        return "Misil: de diametro {} y potencia {})".format(self.diametro, self.potencia, self.potencia)
    def __repr__(self):
        return "Misil: de diametro {}y potencia {})".format(self.diametro, self.potencia, self.potencia)
    def __add__(self, other):
        return Misil(self.x + other.x, self.y + other.y, self.z + other.z)



