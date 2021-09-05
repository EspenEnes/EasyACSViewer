import glm
import numpy as np
from dataclasses import dataclass as component
from ACS_ECS.sceneCamera import SceneCamera


@component
class TransformComponent:
    Translation: glm.vec3 =  glm.vec3(0.0, 0.0, 0.0)
    Rotation: glm.vec3 =  glm.vec3(0.0, 0.0, 0.0)
    yaw: float = 0.0
    roll: float = 0.0
    pitch: float = 0.0
    Scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0)

    Up : glm.vec3 = glm.vec3(0.0, 1.0, 0.0)
    Right : glm.vec3  = glm.vec3(1.0, 0.0, 0.0)
    Forward : glm.vec3 = glm.vec3(0.0, 0.0, 0.0)




    def GetTransform(self):

        return glm.translate(glm.mat4(1.0), self.Translation) * self.GetRotation() *  glm.scale(glm.mat4(1.0), self.Scale)

    def GetRotation(self):
        return glm.rotate(glm.mat4(), self.Rotation.x, glm.vec3(1, 0, 0)) * glm.rotate(glm.mat4(), self.Rotation.y, glm.vec3(0, 1, 0)) * glm.rotate(glm.mat4(), self.Rotation.z, glm.vec3(0, 0, 1))


@component
class TagComponent:
    FriendlyName: str = ""

@component
class CameraComponent:
    Camera: SceneCamera = SceneCamera()
    Primary: bool = True

@component
class SpriteRendererComponent:
    color = (1.0, .5, 1.0, 1.0)

@component
class MeshComponent:
    Vertesies = np.zeros(0, dtype=np.float32)
    Indesies = np.zeros(0, dtype=np.float32)

@component
class RenderComponent:
    Visible : bool = False

class LightComponent:
    color = (1,1,1)

class AcsBoxComponent:
    Xmax : float = 0.0
    Xmin: float = 0.0
    Ymax: float = 0.0
    Ymin: float = 0.0
    Zmax: float = 0.0
    Zmin: float = 0.0

