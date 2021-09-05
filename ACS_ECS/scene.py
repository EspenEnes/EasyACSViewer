from math import sin, cos

import numpy as np
from esper import World, Processor

from ACS_ECS.components import *
from ACS_ECS.entity import Entity
from myopenglDir.ACSBoxRenderer import ACS_Renderer
from myopenglDir.skyboxrenderer import SkyBoxRenderer
from myopenglDir.texture import CubeMap, Texture


class Scene():
    def __init__(self):
        self.scene = World()
        self.scene.add_processor(self.OnUpdateProcessor(self, self.scene))

    def CreateEntity(self, name="NoName"):
        entity = Entity(self.scene.create_entity(), self.scene)
        entity.AddComponent(TransformComponent())
        entity.AddComponent(TagComponent(FriendlyName=name))
        return entity

    def DestroyEntity(self, Entity: Entity):
        self.scene.delete_entity(Entity.entity)

    def OnViewportResize(self, width, height):
        for ent, (camera,) in self.scene.get_components(CameraComponent):
            camera.Camera.SetViewportSize(width, height)

    def GetPrimaryCameraEntity(self):
        for ent, (camera,) in self.scene.get_components(CameraComponent):
            if camera.Primary:
                return ent
            return None

    class OnUpdateProcessor(Processor):
        def __init__(self, parent, scene):
            super().__init__()
            self.direction = glm.vec3(0, 0, 0)
            # self.renderer: ACS_Renderer  = renderer
            self.renderer = ACS_Renderer()
            self.skyboxRenderer = SkyBoxRenderer()

            self.scene = scene

            self.WhiteTexture = CubeMap()
            self.SkyMapTexture = CubeMap("res/textures/Skybox")
            self.tileTexture = Texture("res/textures/Tile.png", repeat=True)

        def process(self, *args, **kwargs):
            mainCamera = None
            cameraTransform = None

            for ent, (trans, camera,) in self.scene.get_components(TransformComponent, CameraComponent):

                trans: TransformComponent
                if camera.Primary:

                    self.m_Position = trans.Translation
                    cameraTransform = glm.lookAt(trans.Translation, trans.Translation + trans.Forward, trans.Up)
                    mainCamera = camera.Camera
                    break

            for ent, (tag, mesh,) in self.scene.get_components(TagComponent, MeshComponent):
                tag: TagComponent
                mesh: MeshComponent
                if tag.FriendlyName == "Skybox":
                    self.skyboxRenderer.BeginScene(mainCamera, cameraTransform)
                    self.SkyMapTexture.Bind()
                    indesies = [x + self.skyboxRenderer.IndexCount for x in mesh.Indesies]
                    vertesies = mesh.Vertesies
                    self.skyboxRenderer.Push_Buffers(np.array(vertesies, dtype=np.float32),
                                                     np.array(indesies, dtype=np.int32))

                    self.skyboxRenderer.IndexCount += mesh.Indesies[-1] + 1

                    self.skyboxRenderer.EndScene()
                    break

            if mainCamera is not None:
                self.WhiteTexture.Bind()
                self.renderer.BeginScene(mainCamera, cameraTransform)
                self.renderer.shader.SetUniform3fv("u_lightPos", np.array(self.m_Position))
                for ent, (ren, mesh,) in self.scene.get_components(RenderComponent, MeshComponent):
                    ren: RenderComponent
                    if not ren.Visible: continue
                    indesies = [x + self.renderer.IndexCount for x in mesh.Indesies]
                    vertesies = mesh.Vertesies
                    self.renderer.Push_Buffers(np.array(vertesies, dtype=np.float32),
                                               np.array(indesies, dtype=np.int32))

                    self.renderer.IndexCount += mesh.Indesies[-1] + 1

                self.renderer.EndScene()


if __name__ == '__main__':
    scene = Scene()
    Camera = scene.CreateEntity("Bolle")
    Camera.AddComponent(CameraComponent())
    scene.GetPrimaryCameraEntity()
