from array import array
from moderngl import LINE_STRIP_ADJACENCY
import numpy as np

_STEPS = 64

class Spline():

    def __init__(self, start = (0,0), cp1=(100,0), cp2=(0,100), end=(100,100) , tint = (1,1,1,1) ):
        for arg_name, arg_value in locals().items():
            if arg_name != 'self':
                setattr(self, arg_name, arg_value)


    def render(self, ctx):
        self.program["linewidth"].value = 4
        self.program["antialias"].value = 2
        self.program["miter_limit"].value = -1
        self.program["color"].value = self.tint
        self.generate_spline()

        Spline.vao.render(mode=LINE_STRIP_ADJACENCY)

    def generate_spline(self):
        points = np.array([
            self.start,  # Start point
            self.cp1,  # Control point 1
            self.cp2,  # Control point 2
            self.end   # End point
        ], dtype=np.float32)

        t = np.linspace(0, 1, _STEPS)

        b0 = (1 - t) ** 3
        b1 = 3 * t * (1 - t) ** 2
        b2 = 3 * t ** 2 * (1 - t)
        b3 = t ** 3
        Spline.point_data.write(array("f",self.start))
        Spline.point_data.write(array("f",self.end),(_STEPS+2)*8)
        for i in range(_STEPS):
            point = np.sum(points * np.array([b0[i], b1[i], b2[i], b3[i]]).reshape(-1, 1), axis=0)
            Spline.point_data.write(array("f", point),(i+1)*8)


    def load_program(main):
        
        Spline.program = main.load_program("rich_lines.glsl")

        # while we're at it set up the geom buffer
        Spline.point_data_size = (_STEPS+3) * 2 * 4  # 2 32 bit floats per step
        Spline.point_data = main.ctx.buffer(reserve=Spline.point_data_size)  # Capacity for 1 spline
        Spline.vao = main.ctx.vertex_array(
            Spline.program,
            [
                (Spline.point_data, "2f", "position"),
            ]
        )
        

