from myopenglDir.baseRenderer import BaseRenderer
from myopenglDir.indexbuffer import IndexBuffer
from myopenglDir.shader import Shader
from myopenglDir.vertexArray import VertexArray
from myopenglDir.vertexbuffer import VertexBuffer
from myopenglDir.vertexbufferlayout import VertexBufferlayout


class ACS_Renderer(BaseRenderer):
    def __init__(self):
        super(ACS_Renderer, self).__init__()
        self.va = VertexArray()
        self.vb = VertexBuffer(size=self.MaxVertexCont)
        self.renderer = self
        self.camera = False

        layout = VertexBufferlayout()
        layout.PushFloat(3)  # Add 3 floats for position
        layout.PushFloat(3)  # Add 3 floats for normals
        layout.PushFloat(4)  # Add 4 floats for color
        layout.PushFloat(1)  # Add 1 floats for EntityId

        self.va.AddBuffer(self.vb, layout)

        self.ib = IndexBuffer(size=self.MaxIndexCont)

        self.shader = Shader("myopenglDir/shader/shader.glsl")
        self.shader.Bind()