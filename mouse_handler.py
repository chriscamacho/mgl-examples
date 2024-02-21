
from moderngl_window.context.base.window import MouseButtons
import numpy as np

class MouseHandler():
    def __init__(self):
        self.screen_offset = ( -(self.window_size[0]/self.window_size[0]), 
                                -(self.window_size[1]/self.window_size[1]))
        self.mouse_pos = (0,0)
        self.mouse_left_down = False
        self.mouse_middle_down = False
        self.mouse_right_down = False
        self.zoom_level = 1

    # unproject and correct mouse (window) coords to "world space"
    def scale_mouse(self, x, y):
        width, height = self.window_size

        ortho_matrix_inv = np.linalg.inv(self.projection)
        
        mouse_window_coords = np.array([x/(width/2)-1, -y/(height/2)+1, 0, 1])
        mouse_frame_coords = np.matmul(ortho_matrix_inv, mouse_window_coords)
        
        # because the mouse coords are not panned, but inverse matrix
        # has panning, we need to allow for this.
        self.mouse_pos = (mouse_frame_coords[0] - self.screen_offset[0]*width/2,
                            mouse_frame_coords[1] - self.screen_offset[1]*height/2)


    # zoom
    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.zoom_level += (y_offset / 10.0)
        if self.zoom_level < 0.1:
            self.zoom_level = 0.1
    
    # when we get a mouse event, convert and store mouse position    
    def mouse_position_event(self, x, y, dx, dy):
        self.scale_mouse(x, y)

    # drag left mouse for control point (sprite) or middle button to pan
    def mouse_drag_event(self, x, y, dx, dy):
        self.scale_mouse(x, y)
        if self.mouse_left_down:
            for s in self.sprites:
                if s.dragging:
                    s.pos = (self.mouse_pos[0] + s.offsetx, self.mouse_pos[1] + s.offsety)
        if self.mouse_middle_down:
            self.screen_offset = (self.screen_offset[0] + (dx/self.window_size[0])*2,
                                self.screen_offset[1] - (dy/self.window_size[1])*2)

    # record buttons start dragging, if intersection with sprite
    def mouse_press_event(self, x, y, button):

        if button == MouseButtons.middle:
            self.mouse_middle_down = True
        if button == MouseButtons.right:
            self.mouse_right_down = True
            
        if button == MouseButtons.left:
            if self.mouse_left_down:
                return # only ever start drag once per drag...
            for s in self.sprites:
                if s.inBounds(self.mouse_pos[0], self.mouse_pos[1]):
                    s.dragging = True
                    s.offsetx = s.pos[0] - self.mouse_pos[0]
                    s.offsety = s.pos[1] - self.mouse_pos[1]
                else:
                    s.dragging = False
            self.mouse_left_down = True

    # update buttons and release dragging
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


    # update window size for scale_mouse
    def resize(self, width, height):
        self.window_size = (width, height)
