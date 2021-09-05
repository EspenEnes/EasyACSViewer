from myopenglDir.baseRenderer import BaseRenderer
from myopenglDir.indexbuffer import IndexBuffer
from myopenglDir.shader import Shader
from myopenglDir.vertexArray import VertexArray
from myopenglDir.vertexbuffer import VertexBuffer
from myopenglDir.vertexbufferlayout import VertexBufferlayout
import numpy as np


class SkyBoxRenderer(BaseRenderer):
    MaxQuadCont = 2000000
    MaxVertexCont = MaxQuadCont * 4
    MaxIndexCont = MaxQuadCont * 6
    MaxTextures = 32

    def __init__(self, path=None):
        super(SkyBoxRenderer, self).__init__()
        self.va = VertexArray()
        self.vb = VertexBuffer(size=self.MaxVertexCont)

        layout = VertexBufferlayout()
        layout.PushFloat(3)  # Add 3 floats for position

        self.va.AddBuffer(self.vb, layout)

        self.ib = IndexBuffer(size=self.MaxIndexCont)

        self.shader = Shader("myopenglDir/shader/SkyboxShader.glsl")
        self.shader.Bind()

    def BeginScene(self, camera = None, transform =None):

        self.shader.Bind()
        self.va.Bind()
        self.vb.Bind()
        self.ib.Bind()

        self.Viewmatrix = np.matrix(transform)
        self.Viewmatrix.itemset((0, 3), 0.0)
        self.Viewmatrix.itemset((1, 3), 0.0)
        self.Viewmatrix.itemset((2, 3), 0.0)

        if transform is not None:
            self.GetViewProjectionMatrix = camera.ProjectionMatrix * self.Viewmatrix
        else:
            self.GetViewProjectionMatrix = camera.ViewProjectionMatrix




        self.shader.SetUniformMath4f("u_ViewProjection", self.GetViewProjectionMatrix)
        self.StartBatch()
