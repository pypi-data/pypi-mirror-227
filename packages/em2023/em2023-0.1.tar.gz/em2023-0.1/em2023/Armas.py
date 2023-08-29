class Misil:
    def __init__(self, x=10, y=10, z=10):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return "Misil: ({}, {}, {})".format(self.x, self.y, self.z)
    def __repr__(self):
        return "Misil: ({}, {}, {})".format(self.x, self.y, self.z)
    def __add__(self, other):
        return Misil(self.x + other.x, self.y + other.y, self.z + other.z)