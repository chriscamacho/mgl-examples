#!/usr/bin/env python

from activate import activate
activate("venv", "python3.12")

import moderngl
from config import Config

from pyrr import Matrix44
from spline import Spline

class SplineRenderer(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ctx.line_width = 4
        width, height = self.ctx.fbo.size
        self.width = width
        self.height = height

        Spline.load_program(self)

        self.splines = []

        s = Spline()
        self.splines.append(s)

        s = Spline( (200,100), (200,100), (200,400), (600,400) )
        s.tint = (1,0,0,1)
        self.splines.append(s)



    def render(self, time, frame_time):
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.ctx.clear(0.1,0.2,0.4)

        # update shaders projection matrix
        projection = Matrix44.orthogonal_projection(
            # left, right, top, bottom, near, far
            0, self.width, self.height, 0, 1, -1, dtype="f4",
            # ensure we create 32 bit value (64 bit is default)
        )
        Spline.program["projection"].write(projection)

        for s in self.splines:
            s.render(self.ctx)


if __name__ == "__main__":
    SplineRenderer.run()
