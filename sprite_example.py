#!/usr/bin/env python

from activate import activate
activate("venv", "python3.12")

"""
based on the geometry shader example, this reduces it to one sprite at
a time so that individual properties like texture and tint can be set
per sprite
"""
import math

import moderngl
from moderngl_window.context.base.window import MouseButtons
from config import Config
import numpy as np
from pyrr import Matrix44
from sprite import Sprite

class Main(Config):

# ----------------------------------------------------------------------
#       initialisation
# ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.cursor = True
        
        num_sprites = 16
        self.mousex = 0
        self.mousey = 0
        self.mouse_pressed = False
        self.a_down = False
        self.z_down = False

        textures = self.load_texture_array(
            'atlas.png', layers=6, mipmap=True, anisotrpy=8.0)

        Sprite.load_textures(self, textures)

        width, height = self.ctx.fbo.size

        # create a list of sprites giving them an initial position
        self.sprites = []

        a = 0
        for i in range(num_sprites):
            a = a + (2*math.pi / num_sprites)
            s = Sprite()

            s.pos_ang = a       # added instance variables
            s.dragging = False
            s.offsetx = 0
            s.offsety = 0

            s.tex = i % 4 + 2
            if s.tex == 0:
                s.rot = 45
            if s.tex == 2:
                s.size = (s.size[0] * 2, s.size[1] * 2)
                s.tint = (1,0,0,0.6)
            s. pos = ( width/2 + math.cos(s.pos_ang*3)*width/3,
                height/2 + math.sin(s.pos_ang)*height/3)

            self.sprites.append(s)
            
        self.mouse_sprite = Sprite()
        self.mouse_sprite.size=(32,32)
        self.mouse_sprite.tint = 1, 0.2, 0.4, 1
        self.mouse_sprite.tex = 0
        
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
            0, width, height, 0, 1, -1, dtype="f4",  # ensure we create 32 bit value (64 bit is default)
        )
        left = -width / 2
        right = width / 2
        bottom = -height / 2
        top = height / 2        
        projection = np.array([
            [2/(right-left), 0,              0, -(right+left)/(right-left)],
            [0,              2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
            [0,              0,             -2, 0],
            [0,              0,              0, 1]
        ], dtype=np.float32)
        
        Sprite.program["projection"].write(projection)

        for s in self.sprites:
            s.pos_ang = s.pos_ang + 0.002 # keep in step if reset
            # only move about if never dragged
            if s.offsetx == 0 and s.offsety == 0:

                s. pos = ( math.cos(s.pos_ang*3)*width/3,
                            math.sin(s.pos_ang)*height/3)

                if s.tex == 3:
                    s.size = (s.size[0], 128 + math.sin(s.pos_ang*2) * 64)

                if s.tex == 1:
                    s.rot = math.cos(s.pos_ang*3)*45

            # tint red if mouse is over sprite
            if s.inBounds(self.mousex, self.mousey):
                s.tint = (1,0,0,s.tint[3])
            else:
                s.tint = (1,1,1,s.tint[3])

            s.render()
        self.mouse_sprite.pos = (self.mousex + 16, self.mousey - 16)
        self.mouse_sprite.render()
        
# ----------------------------------------------------------------------
#       event handling
# ----------------------------------------------------------------------
    # update window size for scale_mouse
    def resize(self, width, height):
        self.window_size = (width, height)

    # fbo never seems to resize, even when window resizes
    def scale_mouse(self, x, y):
        width, height = self.window_size
        fbo_width, fbo_height = self.ctx.fbo.size
        self.mousex = x / (width / fbo_width ) - ((width/2)/(width / fbo_width ))
        self.mousey = -y / (height /fbo_height ) + ((height/2)/(height /fbo_height))

    def key_event(self, key, action, modifiers):
        self.a_down = False
        self.z_down = False
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                # reset all to never dragged
                for s in self.sprites:
                    s.offsetx = 0
                    s.offsety = 0

            if key == self.wnd.keys.A:
                self.a_down = True
            if key == self.wnd.keys.Z:
                self.z_down = True

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        for s in self.sprites:
            if s.inBounds(self.mousex, self.mousey):
                if self.a_down and not self.z_down:
                    s.size = (s.size[0] + y_offset, s.size[1])
                if not self.a_down and self.z_down:
                    s.size = (s.size[0], s.size[1] + y_offset)
                if not self.a_down and not self.z_down:
                    s.rot += y_offset

    # record mouse position
    def mouse_position_event(self, x, y, dx, dy):
        self.scale_mouse(x,y)

    # move any draggies
    def mouse_drag_event(self, x, y, dx, dy):
        self.scale_mouse(x,y)
        for s in self.sprites:
            if s.dragging:
                s.pos = (self.mousex + s.offsetx, self.mousey + s.offsety)

    # start dragging any under mouse
    def mouse_press_event(self, x, y, button):
        if button == MouseButtons.left:
            if self.mouse_pressed:
                return
            for s in self.sprites:
                if s.inBounds(self.mousex, self.mousey):
                    s.dragging = True
                    s.offsetx = s.pos[0] - self.mousex
                    s.offsety = s.pos[1] - self.mousey
                else:
                    s.dragging = False
            self.mouse_pressed = True

    # stop dragging
    def mouse_release_event(self, x: int, y: int, button: int):
        if button == MouseButtons.left:
            for s in self.sprites:
                s.dragging = False
            self.mouse_pressed = False

if __name__ == "__main__":
    Main.run()
