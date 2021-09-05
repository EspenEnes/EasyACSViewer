
from myopenglDir.indexbuffer import IndexBuffer
from myopenglDir.shader import Shader
from myopenglDir.vertexArray import VertexArray
from myopenglDir.vertexbuffer import VertexBuffer
from myopenglDir.vertexbufferlayout import VertexBufferlayout

import glm
import numpy as np
from OpenGL.GL import *


class BaseRenderer():
    MaxQuadCont = 2000000
    MaxVertexCont = MaxQuadCont * 4
    MaxIndexCont = MaxQuadCont * 6
    MaxTextures = 32

    def __init__(self):

        self.va = VertexArray()
        self.vb = VertexBuffer(size=self.MaxVertexCont)
        self.renderer = self
        self.camera = False

        layout = VertexBufferlayout()
        layout.PushFloat(3)  # Add 3 floats for position


        self.va.AddBuffer(self.vb, layout)

        self.ib = IndexBuffer(size=self.MaxIndexCont)

        self.shader = Shader("myopenglDir/shader/shader.glsl")
        self.shader.Bind()
        self.shader.SetUniform1iv("u_Textures", np.array(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
             29, 30, 31], dtype=np.uint))

    def BeginScene(self, camera = None, transform =None ):


        self.shader.Bind()
        self.va.Bind()
        self.vb.Bind()
        self.ib.Bind()

        if camera is not None:
            self.camera = True
            if transform is not None:

                self.GetProjectionMatrix = camera.ProjectionMatrix
                self.GetViewMatrix = np.matrix(transform)



            else:
                self.GetProjectionMatrix = camera.ProjectionMatrix
                self.GetViewMatrix = camera

            self.shader.SetUniformMath4f("u_Projection", self.GetProjectionMatrix)
            self.shader.SetUniformMath4f("u_View", self.GetViewMatrix)
            self.shader.SetUniformMath4f("u_Model", np.matrix(glm.mat4(1.0)))





        self.StartBatch()

    def StartBatch(self):
        self.IndexCount = 0
        self.IndexBufferPtr = 0
        self.VertexBufferPtr = 0
        self.TextureSlotIndex = 1

    def NextBatch(self):
        self.Flush()
        self.StartBatch()

    def Flush(self, transform=np.matrix(glm.mat4(1.0))):
        if self.IndexCount == 0: return

        glBufferData(target=GL_ARRAY_BUFFER, size=self.VertexBufferPtr * 4, data=None, usage=GL_DYNAMIC_DRAW)
        glBufferData(target=GL_ELEMENT_ARRAY_BUFFER, size=self.IndexBufferPtr * 4, data=None, usage=GL_DYNAMIC_DRAW)

        self.shader.Bind()
        if self.camera:
            self.shader.SetUniformMath4f("u_Projection", self.GetProjectionMatrix)
            self.shader.SetUniformMath4f("u_View", self.GetViewMatrix)
            self.shader.SetUniformMath4f("u_Model", np.matrix(glm.mat4(1.0)))



        self.vb.SetData(self.vb.Buffer[0:self.VertexBufferPtr])
        self.ib.SetData(self.ib.Buffer[0:self.IndexBufferPtr])
        glDrawElements(GL_TRIANGLES, self.ib.GetCount(), GL_UNSIGNED_INT, None)

    def Submit(self, Vertecies, Indeces, transform=np.matrix(glm.mat4(1.0))):
        self.shader.Bind()

        if self.camera:
            self.shader.SetUniformMath4f("u_Projection", self.GetProjectionMatrix)
            self.shader.SetUniformMath4f("u_View", self.GetViewMatrix)
            self.shader.SetUniformMath4f("u_Model", np.matrix(glm.mat4(1.0)))

        # self.va.Bind()

        glBufferData(target=GL_ARRAY_BUFFER, size=len(Vertecies) * 4, data=None, usage=GL_DYNAMIC_DRAW)

        glBufferSubData(target=GL_ARRAY_BUFFER, offset=0, data=Vertecies)
        glBufferSubData(target=GL_ELEMENT_ARRAY_BUFFER, offset=0, data=Indeces)

        glDrawElements(GL_TRIANGLES, self.ib.GetCount(), GL_UNSIGNED_INT, None)

    def Push_Buffers(self, Vertecies, Indeces):
        Vertecies = np.array(Vertecies, dtype=np.float32)
        if self.VertexBufferPtr + len(Vertecies) < len(self.vb.Buffer):
            self.vb.Buffer[self.VertexBufferPtr:self.VertexBufferPtr + Vertecies.shape[0]] = Vertecies
            self.VertexBufferPtr += Vertecies.shape[0]

            self.ib.Buffer[self.IndexBufferPtr:self.IndexBufferPtr + Indeces.shape[0]] = Indeces
            self.IndexBufferPtr += Indeces.shape[0]


        elif self.VertexBufferPtr + len(Vertecies) == len(self.vb.Buffer):
            self.vb.Buffer[self.VertexBufferPtr:self.VertexBufferPtr + Vertecies.shape[0]] = Vertecies
            self.VertexBufferPtr += Vertecies.shape[0]

            self.ib.Buffer[self.IndexBufferPtr:self.IndexBufferPtr + Indeces.shape[0]] = Indeces
            self.IndexBufferPtr += Indeces.shape[0]

            self.NextBatch()

        elif self.VertexBufferPtr + len(Vertecies) > len(self.vb.Buffer):
            self.NextBatch()

    def EndScene(self):

        self.Flush()

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


