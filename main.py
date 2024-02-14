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
        
        num_sprites = 64
        self.mousex = 0
        self.mousey = 0
        
        textures = []
        textures.append(self.load_texture_2d("crate.png"))
        textures.append(self.load_texture_2d("checked.png"))
        textures.append(self.load_texture_2d("steel.png"))
        textures.append(self.load_texture_2d("brick.png"))
        
        Sprite.load_textures(self, textures)

        width, height = self.ctx.fbo.size
        
        self.sprites = []
        a = 0
        for i in range(num_sprites):
            a = a + (2*math.pi / num_sprites)
            s = Sprite()
            s.pos_ang = a # added instance variable    
            s.tex = i % 4
            if s.tex == 2:
                s.size = (s.size[0] * 2, s.size[1] * 2)
                s.tint = (1,0,0,0.6)
            self.sprites.append(s)
              
        

    def render(self, time, frame_time):
        self.ctx.clear(0.1,0.2,0.4)
        self.ctx.enable(moderngl.BLEND)

        width, height = self.ctx.fbo.size

        projection = Matrix44.orthogonal_projection(
            # left, right, top, bottom, near, far
            0, width, height, 0, 1, -1, dtype="f4",  # ensure we create 32 bit value (64 bit is default)
        )
        Sprite.program["projection"].write(projection)
               
        for s in self.sprites:
            
            s.pos_ang = s.pos_ang + 0.002
            s. pos = ( width/2 + math.cos(s.pos_ang*3)*width/3,
                        height/2 + math.sin(s.pos_ang)*height/3)
            
            if s.tex == 3: 
                s.size = (s.size[0], 128 + math.sin(s.pos_ang*2) * 64)
                
            if s.tex == 1:
                s.rot = math.cos(s.pos_ang*3)*45
            
            if s.inBounds(self.mousex, self.mousey):
                s.tint = (1,0,0,s.tint[3])
            else:
                s.tint = (1,1,1,s.tint[3])
            
            s.render()
    
    def mouse_position_event(self, x, y, dx, dy):
        self.mousex = x
        self.mousey = y

if __name__ == "__main__":
    Main.run()
