from array import array
from moderngl import LINE_STRIP
from math import radians, cos, sin
from pyrr import Matrix44, Vector3
import numpy as np

_STEPS = 8

class Spline():
    
    def __init__(self, start = (0,0), cp1=(100,0), cp2=(0,100), end=(100,100) , tint = (1,1,1,1) ):
        for arg_name, arg_value in locals().items():
            if arg_name != 'self': setattr(self, arg_name, arg_value)

        
    def render(self, ctx):
        #point_data_size = 2 * 4  # 2 32 bit floats
        #Spline.point_data = ctx.buffer(reserve=(_STEPS * self.point_data_size))
        #Spline.vao = ctx.vertex_array(
        #    Spline.program,
        #    [
        #        (Spline.point_data, "2f", "in_vert"),
        #    ]
        #)
        self.generate_spline()
        
        Spline.program["line_colour"] = self.tint
        Spline.vao.render(mode=LINE_STRIP)

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

        for i in range(_STEPS):
            point = np.sum(points * np.array([b0[i], b1[i], b2[i], b3[i]]).reshape(-1, 1), axis=0)
            Spline.point_data.write(array("f", point),i*8)
            
        
    def load_program(main):
        
        Spline.program = main.load_program("spline.glsl")

        # while we're at it set up the geom buffer
        Spline.point_data_size = _STEPS * 2 * 4  # 2 32 bit floats per step
        Spline.point_data = main.ctx.buffer(reserve=Spline.point_data_size)  # Capacity for 1 spline
        Spline.vao = main.ctx.vertex_array(
            Spline.program,
            [
                (Spline.point_data, "2f", "in_vert"),
            ]
        )
        

