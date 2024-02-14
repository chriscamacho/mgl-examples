from array import array
from moderngl import POINTS

class Sprite():
    
    def __init__(self, pos = (0,0) , size = (128, 64), tex=0, tint = (1,1,1,1) ):
        for arg_name, arg_value in locals().items():
            if arg_name != 'self': setattr(self, arg_name, arg_value)
        self.rot = 0
        
        
    def render(self):
        self.sprite_data.write(array("f", [self.pos[0], self.pos[1], 
                                            self.size[0], self.size[1], self.rot ]))
        self.program["sprite_texture"] = self.tex
        self.program["in_tint"] = self.tint
        Sprite.texture[self.tex].use(self.tex)
        Sprite.vao.render(mode=POINTS, vertices=1)
        
    def load_textures(main, textures):
        
        Sprite.program = main.load_program("sprite.glsl")
        
        Sprite.texture = textures
        
        # bind the textures to the first n texture units
        for i, t in enumerate(Sprite.texture):
            t.use(location=i)
        
        # while we're at it set up the geom buffer
        Sprite.sprite_data_size = 5 * 4  # 5 32 bit floats
        Sprite.sprite_data = main.ctx.buffer(reserve=1 * Sprite.sprite_data_size)  # Capacity for 1 sprite
        Sprite.vao = main.ctx.vertex_array(
            Sprite.program,
            [
                (Sprite.sprite_data, "2f 2f 1f", "in_position", "in_size", "in_rotation"),
            ]
        )

    def inBounds(self, x, y):
        if x > self.pos[0] - self.size[0]/2 and \
            x < self.pos[0] + self.size[0]/2 and \
            y > self.pos[1] - self.size[1]/2 and \
            y < self.pos[1] + self.size[1]/2:
                
            return True
        else:
            return False
             
