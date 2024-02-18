#!/usr/bin/env python

from activate import activate
activate("venv", "python3.12")

"""
based on the geometry shader example, and rich lines example
show enditable splines
"""
import moderngl
from config import Config

from pyrr import Matrix44
from sprite import Sprite
from spline import Spline

from random import uniform as rnd

from mouse_handler import MouseHandler

class Main(MouseHandler, Config):

# ----------------------------------------------------------------------
#       initialisation
# ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        MouseHandler.__init__(self)

        textures = self.load_texture_array(
            'atlas.png', layers=5, mipmap=True, anisotrpy=8.0)

        Sprite.load_textures(self, textures)

        # create a list of sprites
        self.sprites = []
        self.splines = []
        Spline.load_program(self)
        
        starts = [(43, 672), (596, 400), (64, 388), (580, 654)], \
                    [(1190, 57), (672, 48), (1186, 229), (679, 242)], \
                    [(346, 52), (270, 51), (69, 292), (588, 302)], \
                    [(822, 650), (1202, 643), (1067, 367), (938, 365)],

        for i in range(4):
            s = Spline()
            self.splines.append(s)
            start = starts[i]
            s.tint = (rnd(0.5, 1), rnd(0.5, 1), rnd(0.5, 1), 1)
            s.startSprite = Sprite((start[0]), (32,32), 0, tint=(1.0,0,0,1))
            s.endSprite = Sprite((start[1]), (32,32), 0, tint=(0,1.0,0,1))
            s.cp1Sprite = Sprite((start[2]), (32,32), 0, tint=(1.0,1.0,0,1))
            s.cp2Sprite = Sprite((start[3]), (32,32), 0, tint=(0,1.0,1.0,1))
            self.sprites.append(s.startSprite)
            self.sprites.append(s.endSprite)
            self.sprites.append(s.cp1Sprite)
            self.sprites.append(s.cp2Sprite)

        for s in self.sprites:
            s.dragging = False
            s.offsetx = 0
            s.offsety = 0
            s.tex = 0
            s.oldtint = s.tint

# ----------------------------------------------------------------------
#       main render event
# ----------------------------------------------------------------------

    def render(self, time, frame_time):
        self.ctx.clear(0.1,0.2,0.4)
        self.ctx.enable(moderngl.BLEND)

        width, height = self.ctx.fbo.size

        # update shaders projection matrix
        projection = Matrix44.orthogonal_projection(
            # left, right, top, bottom, near, far
            self.screen_offset_x, width + self.screen_offset_x, 
            height + self.screen_offset_y, self.screen_offset_y, 
            1, -1, dtype="f4",
            # ensure we create 32 bit value (64 bit is default)
        )
        Sprite.program["projection"].write(projection)

        for s in self.sprites:
            # dim tint if mouse is over sprite
            if s.inBounds(self.mousex, self.mousey):
                s.tint = (s.oldtint[0]/2,s.oldtint[1]/2,s.oldtint[2]/2,s.tint[3])
            else:
                s.tint = s.oldtint
            s.render()

        Spline.program["projection"].write(projection)
        for s in self.splines:
            # update spline points with its sprite
            s.start = s.startSprite.pos
            s.end = s.endSprite.pos
            s.cp1 = s.cp1Sprite.pos
            s.cp2 = s.cp2Sprite.pos
            s.render(self.ctx)


# ----------------------------------------------------------------------
#       event handling
# ----------------------------------------------------------------------
    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                for s in self.splines:
                    s.print()

    # update window size for scale_mouse
    def resize(self, width, height):
        self.window_size = (width, height)


if __name__ == "__main__":
    Main.run()
    
