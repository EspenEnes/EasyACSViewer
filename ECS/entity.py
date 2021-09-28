import esper

from ECS.components import TransformComponent


class Entity():
    def __init__(self,entity:int, scene:esper.World):
        self.entity = entity
        self.scene = scene

    def AddComponent(self,*args, **kwargs):
        self.scene.add_component(self.entity,*args)

    def GetComponent(self,component):
        return self.scene.component_for_entity(self.entity,component)

    def HasComponents(self):
        return self.scene.components_for_entity(self.entity)

    def RemoveComponent(self, component):
        self.scene.remove_component(self.entity, component)

if __name__ == '__main__':
    scene = esper.World()
    test1 = Entity(scene.create_entity(),scene)
    test1.AddComponent(TransformComponent())
    test1.GetComponent(TransformComponent)






