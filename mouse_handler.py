
from moderngl_window.context.base.window import MouseButtons
import numpy as np

class MouseHandler():
    def __init__(self):
        self.screen_offset_x = -(self.window_size[0]/self.window_size[0])
        self.screen_offset_y = -(self.window_size[1]/self.window_size[1])
        self.mousex = 0
        self.mousey = 0
        self.mouse_left_down = False
        self.mouse_middle_down = False
        self.mouse_right_down = False
        self.zoom_level = 1

    def scale_mouse(self, x, y):
        width, height = self.window_size
        fbo_width, fbo_height = self.ctx.fbo.size

        ortho_matrix_inv = np.linalg.inv(self.projection)
        
        mouse_window_coords = np.array([x/(width/2)-1, -y/(height/2)+1, 0, 1])
        mouse_frame_coords = np.matmul(ortho_matrix_inv, mouse_window_coords)
        
        self.mousex = mouse_frame_coords[0] - self.screen_offset_x*width/2
        self.mousey = mouse_frame_coords[1] - self.screen_offset_y*height/2
        



    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.zoom_level += (y_offset / 10.0)
        
    def mouse_position_event(self, x, y, dx, dy):
        self.scale_mouse(x, y)

    def mouse_drag_event(self, x, y, dx, dy):
        self.scale_mouse(x, y)
        if self.mouse_left_down:
            for s in self.sprites:
                if s.dragging:
                    s.pos = (self.mousex + s.offsetx, self.mousey + s.offsety)
        if self.mouse_middle_down:
            self.screen_offset_x = self.screen_offset_x + (dx/self.window_size[0])*2
            self.screen_offset_y = self.screen_offset_y - (dy/self.window_size[1])*2

    def mouse_press_event(self, x, y, button):
        if button == MouseButtons.left:
            if self.mouse_left_down:
                return
            for s in self.sprites:
                if s.inBounds(self.mousex, self.mousey):
                    s.dragging = True
                    s.offsetx = s.pos[0] - self.mousex
                    s.offsety = s.pos[1] - self.mousey
                else:
                    s.dragging = False
        if button == MouseButtons.left:
            self.mouse_left_down = True
        if button == MouseButtons.middle:
            self.mouse_middle_down = True
        if button == MouseButtons.right:
            self.mouse_right_down = True

    def mouse_release_event(self, x: int, y: int, button: int):
        if button == MouseButtons.left:
            self.mouse_left_down = False
        if button == MouseButtons.middle:
            self.mouse_middle_down = False
        if button == MouseButtons.right:
            self.mouse_right_down = False

        if button == MouseButtons.left:
            for s in self.sprites:
                s.dragging = False
