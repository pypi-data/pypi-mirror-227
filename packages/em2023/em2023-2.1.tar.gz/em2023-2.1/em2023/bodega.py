from random import randint, choice
from hashlib import sha256

STAMENTS = ['activo', 'inactivo']

class Misil:
    def __init__(self, id=0):
        self.id = id
        self.x = randint(0, 255)
        self.y = randint(0, 255)
        self.number = randint(0, 1)
        self._estado = choice(STAMENTS)

    @property
    def estado(self):
        if self._estado == "activo":
            self._estado = "inactivo"
        else:
            self._estado = "activo"
        return self._estado

    def checkImpacto(self, x, y):
        if (self.x == x) and (self.y == y):
            return True
        else:
            return False

    def __str__(self):
        return "Misil: número {})".format(self.id)

    def __repr__(self):
        return "Misil: número {})".format(self.id)

class bodega:
    def __init__(self):
        self.misiles = []
        self.set_x = set()
        self.set_y = set()
        self.cantidad_activos = 0
        self.cantidad_inactivos = 0

    def llenar(self, n):
        for _ in range(n):
            m = Misil()
            while m.x in self.set_x and m.y in self.set_y:
                m = Misil()
            self.misiles.append(m)
            self.set_x.add(m.x)
            self.set_y.add(m.y)
            if m.estado == "activo":
                self.cantidad_activos += 1
            else:
                self.cantidad_inactivos += 1

    def buscar_y_tocar_misil(self, x, y):
        for misil in self.misiles:
            if misil.checkImpacto(x, y):
                estado_actual = misil.estado
                if estado_actual == "activo":
                    self.cantidad_inactivos -= 1
                    self.cantidad_activos += 1
                return True
        return False

    def __str__(self):
        return "Bodega: {} activos, {} inactivos".format(self.cantidad_activos, self.cantidad_inactivos)

    def crear_codigo(self):
        input_str = str(self.cantidad_activos) + str(self.cantidad_inactivos)
        hash_object = sha256(input_str.encode())
        hash_bytes = hash_object.digest()[:8]
        unique_number = int.from_bytes(hash_bytes, byteorder='big')
        return unique_number


global_bodega = bodega()

def crear_bodega(n):
    global global_bodega
    global_bodega = bodega()
    global_bodega.llenar(n)

def buscar_y_tocar_misil(x, y):
    global global_bodega
    return global_bodega.buscar_y_tocar_misil(x, y)

def obtener_activos():
    global global_bodega
    return global_bodega.cantidad_activos

def obtener_codigo():
    global global_bodega
    return global_bodega.crear_codigo()

crear_bodega(10)
print(obtener_activos())
buscar_y_tocar_misil(5, 6)
print(obtener_activos())