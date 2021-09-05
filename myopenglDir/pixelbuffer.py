from OpenGL.GL import *

class PixelBuffer():
    def __init__(self):
        self.PBO = glGenBuffers(1)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, self.PBO )
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self._main_fb)
        glReadBuffer(GL_COLOR_ATTACHMENT0)
