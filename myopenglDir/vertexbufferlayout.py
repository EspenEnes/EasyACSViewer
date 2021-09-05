from OpenGL.GL import *


class VertexBufferlayout():

    @staticmethod
    def GetSizeOfType(type):
        if type == GL_FLOAT:
            return 4
        elif type == GL_UNSIGNED_INT:
            return 4
        elif type == GL_UNSIGNED_BYTE:
            return 1
        else:
            return 0

    def __init__(self):

        self.m_Elements = list()
        self.m_stride = 0

    def PushFloat(self, count):
        VertexBufferElement = {"type": GL_FLOAT, "count": count, "normalized": GL_FALSE}
        self.m_stride += 4 * count
        self.m_Elements.append(VertexBufferElement)

    def PushUINT(self, count):
        VertexBufferElement = {"type": GL_UNSIGNED_INT, "count": count, "normalized": GL_FALSE}
        self.m_stride += 4 * count
        self.m_Elements.append(VertexBufferElement)

    def PushINT(self, count):
        VertexBufferElement = {"type": GL_INT, "count": count, "normalized": GL_FALSE}
        self.m_stride += 4 * count
        self.m_Elements.append(VertexBufferElement)


if __name__ == '__main__':
    vbl = VertexBufferlayout()
    vbl.PushFloat(5)
    vbl.PushFloat(1)
    vbl.PushUINT(1)

    elements = vbl.m_Elements

    for i, element in enumerate(vbl.m_Elements):
        print(i, element["count"], element["type"], element["normalized"], vbl.m_stride, None)
