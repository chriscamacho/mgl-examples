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

from pyrr import Matrix44
from sprite import Sprite

import numpy as np

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
            'atlas.png', layers=4, mipmap=True, anisotrpy=8.0)
        
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

            s.tex = i % 4
            if s.tex == 0:
                s.rot = 45
            if s.tex == 2:
                s.size = (s.size[0] * 2, s.size[1] * 2)
                s.tint = (1,0,0,0.6)
            s. pos = ( width/2 + math.cos(s.pos_ang*3)*width/3,
                height/2 + math.sin(s.pos_ang)*height/3)

            self.sprites.append(s)

        
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
            s.pos_ang = s.pos_ang + 0.002 # keep in step if reset
            # only move about if never dragged
            if s.offsetx == 0 and s.offsety == 0:
                
                s. pos = ( width/2 + math.cos(s.pos_ang*3)*width/3,
                            height/2 + math.sin(s.pos_ang)*height/3)
                
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
        self.leftSft = False
        self.leftCtr = False
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                # reset all to never dragged
                for s in self.sprites:
                    s.offsetx = 0
                    s.offsety = 0

            if key == self.wnd.keys.A:
                self.leftSft = True
            if key == self.wnd.keys.Z:
                self.leftCtr = True
    
    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        for s in self.sprites:
            if s.inBounds(self.mousex, self.mousey):
                if self.leftSft and not self.leftCtr:
                    s.size = (s.size[0] + y_offset, s.size[1]) 
                if not self.leftSft and self.leftCtr:
                    s.size = (s.size[0], s.size[1] + y_offset)
                if not self.leftSft and not self.leftCtr:
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
