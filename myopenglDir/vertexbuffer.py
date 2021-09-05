import numpy as np
from OpenGL.GL import *


class VertexBuffer():
    def __init__(self, data=None, size=None):

        self.m_RenderID = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.m_RenderID)
        if data is not None:
            glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        else:
            glBufferData(target=GL_ARRAY_BUFFER, size=size * 40, data=None, usage=GL_DYNAMIC_DRAW)
            self.Buffer = np.zeros((int((size / 4) * 40),), dtype=np.float32)

    def SetData(self, data=None):
        # if data == None: data = self.Buffer
        self.Bind()
        glBufferSubData(target=GL_ARRAY_BUFFER, offset=0, data=data)

    #
    def Bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.m_RenderID)

    def UnBind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)
