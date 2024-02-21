import os

import moderngl_window as mglw


class Config(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Example"
    window_size = (1280, 720)
    resizable = True
    vsync = True
    resource_dir = os.path.normpath(os.path.join(__file__, '../data'))
    cursor = False


