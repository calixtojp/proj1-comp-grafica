from lua import Lua

class Objetos:
    def __init__(self):
        # Inicializa a lua com raio 1.0 e 36 segmentos
        self.lua = Lua(radius=1.0, num_segments=36)

    def draw(self):
        self.lua.draw()

    def rotate(self, speed_x=0.01, speed_y=0.01, speed_z=0.01):
        self.lua.rotate(speed_x, speed_y, speed_z)
