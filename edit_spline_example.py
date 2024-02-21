#!/usr/bin/env python

from activate import activate
activate("venv", "python3.12")

"""
based on the geometry shader example, and rich lines example
show enditable splines
"""
import moderngl
from moderngl_window.text.bitmapped import TextWriter2D
from config import Config

from pyrr import Matrix44
from sprite import Sprite
from spline import Spline

from random import uniform as rnd

from mouse_handler import MouseHandler

import numpy as np


class Main(MouseHandler, Config):

# ----------------------------------------------------------------------
#       initialisation
# ----------------------------------------------------------------------
    
    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        MouseHandler.__init__(self)

        textures = self.load_texture_array(
            'atlas.png', layers=6, mipmap=True, anisotrpy=8.0)

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
            s.tex = 1
            s.oldtint = s.tint
            
        self.mouseSprite = Sprite()
        self.mouseSprite.size=(32,32)
        self.mouseSprite.tint = 1, 0.2, 0.4, 1
        self.mouseSprite.tex = 0
        
        self.writer = TextWriter2D()

# ----------------------------------------------------------------------
#   Prespective Matrix, combines zoom, panning & perspective 
# ----------------------------------------------------------------------
    def calc_perspective(self):
        width, height = self.window_size

        # Calculate zoom and offset matrices
        zoom_matrix = np.array([
            [1/self.zoom_level, 0, 0, 0],
            [0, 1/self.zoom_level, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        offset_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [self.screen_offset[0], self.screen_offset[1], 0, 1]
        ], dtype=np.float32)

        # Calculate orthogonal projection matrix
        left = -width / 2
        right = width / 2
        bottom = -height / 2
        top = height / 2
        projection_matrix = np.array([
            [2/(right-left), 0,              0, -(right+left)/(right-left)],
            [0,              2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
            [0,              0,             -2, 0],
            [0,              0,              0, 1]
        ], dtype=np.float32)

        transformation_matrix = np.matmul(offset_matrix, zoom_matrix)
        self.projection = np.matmul(projection_matrix, transformation_matrix)

        
# ----------------------------------------------------------------------
#       main render event
# ----------------------------------------------------------------------

    def render(self, time, frame_time):
        self.ctx.clear(0.1,0.2,0.4)
        self.ctx.enable(moderngl.BLEND)

        self.calc_perspective()

        Sprite.program["projection"].write(self.projection)

        for s in self.sprites:
            # dim tint if mouse is over sprite
            if s.inBounds(self.mouse_pos[0], self.mouse_pos[1]):
                s.tint = (s.oldtint[0]/2,s.oldtint[1]/2,s.oldtint[2]/2,s.tint[3])
            else:
                s.tint = s.oldtint
            s.render()
            
        self.mouseSprite.pos = (self.mouse_pos[0] + 16, self.mouse_pos[1] - 16)
        self.mouseSprite.render()

        Spline.program["projection"].write(self.projection)
        for s in self.splines:
            # update spline points with its sprite
            s.start = s.startSprite.pos
            s.end = s.endSprite.pos
            s.cp1 = s.cp1Sprite.pos
            s.cp2 = s.cp2Sprite.pos
            s.render(self.ctx)

        self.writer.text = f"mouse {self.mouse_pos[0]:.2f}, {self.mouse_pos[1]:.2f}"
        self.writer.draw((20, 20), size=20)
        
        self.writer.text = f"zoom {self.zoom_level:.2f}"
        self.writer.draw((20, 40), size=20)

        Sprite.texture.use(location = 0) # reset for sprites
        
# ----------------------------------------------------------------------
#       event handling (mouse events in mouse_handler)
# ----------------------------------------------------------------------
    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                for s in self.splines:
                    s.print()



if __name__ == "__main__":
    Main.run()
    
