import numpy as np
from OpenGL.GL import *


class IndexBuffer():
    def __init__(self, data=None, size=None):
        self.data = data
        self.m_RenderID = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.m_RenderID)
        if data is not None:
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        else:
            glBufferData(target=GL_ELEMENT_ARRAY_BUFFER, size=size * 4, data=None, usage=GL_DYNAMIC_DRAW)
            self.Buffer = np.zeros((size,), dtype=np.int32)
            self.data = self.Buffer

    def SetData(self, data=None):
        # if data == None: data = self.Buffer
        glBufferSubData(target=GL_ELEMENT_ARRAY_BUFFER, offset=0, data=data)

    def GetCount(self):
        return len(self.data)

    def Bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.m_RenderID)

    def UnBind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
