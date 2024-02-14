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
from config import Config

from pyrr import Matrix44
from sprite import Sprite

class Main(Config):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        num_sprites = 16
        self.mousex = 0
        self.mousey = 0
        self.mousePressed = False
        
        textures = []
        textures.append(self.load_texture_2d("crate.png"))
        textures.append(self.load_texture_2d("checked.png"))
        textures.append(self.load_texture_2d("steel.png"))
        textures.append(self.load_texture_2d("brick.png"))
        
        Sprite.load_textures(self, textures)

        width, height = self.ctx.fbo.size
        
        # create a list of sprites giving them an initial position
        self.sprites = []
        a = 0
        for i in range(num_sprites):
            a = a + (2*math.pi / num_sprites)
            s = Sprite()
                
            s.tex = i % 4
            if s.tex == 2:
                s.size = (s.size[0] * 2, s.size[1] * 2)
                s.tint = (1,0,0,0.6)
            s. pos = ( width/2 + math.cos(s.pos_ang*3)*width/3,
                height/2 + math.sin(s.pos_ang)*height/3)
                
                        
            s.pos_ang = a       # added instance variables
            s.dragging = False
            s.offsetx = 0
            s.offsety = 0
            
            self.sprites.append(s)
              
        

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
            # only move about if never dragged
            if s.offsetx == 0 and s.offsety == 0:
                s.pos_ang = s.pos_ang + 0.002
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
    
    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                # reset all to never dragged
                for s in self.sprites:
                    s.offsetx = 0
                    s.offsety = 0
            
    # record mouse position
    def mouse_position_event(self, x, y, dx, dy):
        self.mousex = x
        self.mousey = y
    
    # move any draggies
    def mouse_drag_event(self, x, y, dx, dy):
        self.mousex = x
        self.mousey = y
        for s in self.sprites:
            if s.dragging:
                s.pos = (self.mousex + s.offsetx, self.mousey + s.offsety)       
        
    # start dragging any under mouse
    def mouse_press_event(self, x, y, button):
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
        for s in self.sprites:
            s.dragging = False
        self.mousePressed = False

if __name__ == "__main__":
    Main.run()
