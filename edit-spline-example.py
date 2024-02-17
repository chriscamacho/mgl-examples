#!/usr/bin/env python

from activate import activate
activate("venv", "python3.12")

"""
based on the geometry shader example, and rich lines example
show enditable splines
"""
import math

import moderngl
from moderngl_window.context.base.window import MouseButtons
from config import Config

from pyrr import Matrix44
from sprite import Sprite
from spline import Spline

import numpy as np
from random import uniform as rnd

class Main(Config):

# ----------------------------------------------------------------------
#       initialisation
# ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        num_sprites = 16
        self.mousex = 0
        self.mousey = 0
        self.mousePressed = False
        self.leftSft = False
        self.leftCtr = False
        
        textures = self.load_texture_array(
            'atlas.png', layers=5, mipmap=True, anisotrpy=8.0)
        
        Sprite.load_textures(self, textures)

        width, height = self.ctx.fbo.size
        
        # create a list of sprites
        self.sprites = []

        self.splines = []
        Spline.load_program(self)
        
        for i in range(4):
            s = Spline()
            self.splines.append(s)
            s.tint = (rnd(0.5, 1), rnd(0.5, 1), rnd(0.5, 1), 1)
            s.startSprite = Sprite((rnd(0,width), rnd(0,height)), (32,32), 0, tint=(1.0,0,0,1))
            s.endSprite = Sprite((rnd(0,width), rnd(0,height)), (32,32), 0, tint=(0,1.0,0,1))
            s.cp1Sprite = Sprite((rnd(0,width), rnd(0,height)), (32,32), 0, tint=(1.0,1.0,0,1))
            s.cp2Sprite = Sprite((rnd(0,width), rnd(0,height)), (32,32), 0, tint=(0,1.0,1.0,1))
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
            0, width, height, 0, 1, -1, dtype="f4",  # ensure we create 32 bit value (64 bit is default)
        )
        Sprite.program["projection"].write(projection)
             
        for s in self.sprites:
            # tint red if mouse is over sprite
            if s.inBounds(self.mousex, self.mousey):
                s.tint = (s.oldtint[0]/2,s.oldtint[1]/2,s.oldtint[2]/2,s.tint[3])
            else:
                s.tint = s.oldtint
            
            s.render()
        
        Spline.program["projection"].write(projection)    
        for s in self.splines:
            s.start = s.startSprite.pos
            s.end = s.endSprite.pos
            s.cp1 = s.cp1Sprite.pos
            s.cp2 = s.cp2Sprite.pos
            s.render(self.ctx)
            
    
# ----------------------------------------------------------------------
#       event handling
# ----------------------------------------------------------------------
    # update window size for scale_mouse
    def resize(self, x, y):
        self.window_size = (x,y)
    
    # fbo never seems to resize, even when window resizes
    def scale_mouse(self, x, y):
        width, height = self.window_size
        fbo_width, fbo_height = self.ctx.fbo.size
        self.mousex = x / (width / fbo_width )
        self.mousey = y / (height /fbo_height )

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                pass
    
    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        pass

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
            if self.mousePressed: return
            for s in self.sprites:
                if s.inBounds(self.mousex, self.mousey):
                    s.dragging = True
                    s.offsetx = s.pos[0] - self.mousex
                    s.offsety = s.pos[1] - self.mousey
                    
                else:
                    s.dragging = False
            self.mousePressed = True

    # stop dragging
    def mouse_release_event(self, x: int, y: int, button: int):
        if button == MouseButtons.left:
            for s in self.sprites:
                s.dragging = False
            self.mousePressed = False

if __name__ == "__main__":
    Main.run()
