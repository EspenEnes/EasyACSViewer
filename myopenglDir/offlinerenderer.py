from myopenglDir.baseRenderer import BaseRenderer
from myopenglDir.indexbuffer import IndexBuffer
from myopenglDir.shader import Shader
from myopenglDir.vertexArray import VertexArray
from myopenglDir.vertexbuffer import VertexBuffer
from myopenglDir.vertexbufferlayout import VertexBufferlayout
import numpy as np


class OfflineRenderer(BaseRenderer):
    MaxQuadCont = 2000000
    MaxVertexCont = MaxQuadCont * 4
    MaxIndexCont = MaxQuadCont * 6
    MaxTextures = 32

    def __init__(self, path=None):
        super(OfflineRenderer, self).__init__()
        self.va = VertexArray()
        self.vb = VertexBuffer(size=self.MaxVertexCont)

        layout = VertexBufferlayout()
        layout.PushFloat(2)  # Add 2 floats for position
        layout.PushFloat(2)  # Add 2 floats for Text-cord

        self.va.AddBuffer(self.vb, layout)

        self.ib = IndexBuffer(size=self.MaxIndexCont)

        self.shader = Shader("myopenglDir/shader/OfflineShader.glsl")
        self.shader.Bind()



    def plainBox(self):

        Vertecies = np.array([
            -1.0, 1.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0,
            1.0, -1.0, 1.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0], dtype=np.float32)

        values = [x + (self.IndexCount) for x in [0, 1, 2, 3, 4, 5]]

        idx = np.array(values, dtype=np.int32)
        self.IndexCount += 6

        self.Push_Buffers(Vertecies, idx)
