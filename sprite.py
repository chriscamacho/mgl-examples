from array import array
from moderngl import POINTS
from math import radians, cos, sin

class Sprite():

    def __init__(self, pos = (0,0) , size = (128, 64), tex=0, tint = (1,1,1,1) ):
        for arg_name, arg_value in locals().items():
            if arg_name != 'self': 
                setattr(self, arg_name, arg_value)

        self.rot = 0


    def render(self):
        self.sprite_data.write(array("f", [self.pos[0], self.pos[1], 
                                            self.size[0], self.size[1], self.rot ]))
        self.program["tex"] = self.tex
        self.program["in_tint"] = self.tint

        Sprite.vao.render(mode=POINTS, vertices=1)

    def load_textures(main, textures):
        Sprite.program = main.load_program("sprite.glsl")

        Sprite.texture = textures
        Sprite.texture.use(location = 0)
        Sprite.program['texture0'].value = 0
        
        # while we're at it set up the geom buffer
        Sprite.sprite_data_size = 5 * 4  # 5 32 bit floats
        Sprite.sprite_data = main.ctx.buffer(reserve=1 * Sprite.sprite_data_size)  # Capacity for 1 sprite
        Sprite.vao = main.ctx.vertex_array(
            Sprite.program,
            [
                (Sprite.sprite_data, "2f 2f 1f", "in_position", "in_size", "in_rotation"),
            ]
        )

    def reverse_rotate_point(self, x, y):
        # Translate the point so that the center of rotation is at the origin
        translated_x = x - self.pos[0]
        translated_y = y - self.pos[1]

        # Convert the rotation angle to radians
        angle = radians(self.rot)

        # Calculate the cosine and sine of the reverse angle
        reverse_cos = cos(-angle)
        reverse_sin = sin(-angle)

        # Apply the reverse rotation to the translated point
        reversed_x = translated_x * reverse_cos - translated_y * reverse_sin
        reversed_y = translated_x * reverse_sin + translated_y * reverse_cos

        # Translate the point back to its original position
        reversed_x += self.pos[0]
        reversed_y += self.pos[1]

        return reversed_x, reversed_y

    def inBounds(self, x, y):
        (x, y) = self.reverse_rotate_point(x, y)
        if x > self.pos[0] - self.size[0]/2 and \
            x < self.pos[0] + self.size[0]/2 and \
            y > self.pos[1] - self.size[1]/2 and \
            y < self.pos[1] + self.size[1]/2:

            return True
        return False
