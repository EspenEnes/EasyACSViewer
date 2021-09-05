from OpenGL.GL import *

from myopenglDir.vertexbuffer import VertexBuffer
from myopenglDir.vertexbufferlayout import VertexBufferlayout


class VertexArray():
    def __init__(self):
        self.m_RenderID = glGenVertexArrays(1)
        self.offsett = 0

    def AddBuffer(self, vb: VertexBuffer, layout: VertexBufferlayout):
        self.Bind()
        vb.Bind()

        for i, element in enumerate(layout.m_Elements):
            glEnableVertexAttribArray(i)
            # print(i, element["count"], element["type"], element["normalized"], layout.m_stride, self.offsett)
            if element["type"] == GL_INT or element["type"] == GL_UNSIGNED_INT :
                glVertexAttribIPointer(i,element["count"], element["type"],layout.m_stride,ctypes.c_void_p(self.offsett))
            else:
                glVertexAttribPointer(i, element["count"], element["type"], element["normalized"], layout.m_stride,
                                  ctypes.c_void_p(self.offsett))
            self.offsett += element["count"] * VertexBufferlayout.GetSizeOfType(element["type"])

    def Bind(self):
        glBindVertexArray(self.m_RenderID)

    def UnBind(self):
        glBindVertexArray(0)
