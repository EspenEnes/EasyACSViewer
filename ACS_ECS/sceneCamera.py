from math import cos, sin

import glm
import numpy as np


class SceneCamera():
    def __init__(self):
        self.m_Projection = np.matrix(glm.mat4(1.0))

        self.m_PerspectiveFOV = glm.radians(45.0)
        self.m_PerspectiveNear = 0.1
        self.m_PerspectiveFar = 1000.0

        self.m_AspectRatio = 0.0

        self.RecalculateProjection()

    def SetPerspective(self,FOV,nearClip, farClip):
        self.m_PerspectiveFOV = glm.radians(FOV)
        self.m_PerspectiveNear = nearClip
        self.m_PerspectiveFar = farClip
        self.RecalculateProjection()

    def SetViewportSize(self, width:float, height:float):
        self.m_AspectRatio = width / height

        self.RecalculateProjection()

    @property
    def ProjectionMatrix(self):
        self.RecalculateProjection()
        return self.m_Projection

    def RecalculateProjection(self):
        self.m_Projection = np.matrix(
            glm.perspective(self.m_PerspectiveFOV,self.m_AspectRatio , self.m_PerspectiveNear, self.m_PerspectiveFar),dtype=np.float)

