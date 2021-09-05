from math import cos, sin

from PyQt6 import QtCore
from PyQt6.QtGui import QKeyEvent
import glm


from ACS_ECS.components import *



class CameraController():
    def __init__(self, scene):
        self.scene = scene.scene
        self.fwd : bool = False
        self.bwd: bool = False
        self.left: bool = False
        self.right: bool = False
        self.slewCW : bool = False
        self.slewCCW: bool = False
        self.tiltUp: bool = False
        self.tiltDown: bool = False
        self.up: bool = False
        self.down: bool = False
        self.speed: float = 0.005


    def keypressevent(self, event):
            if event.key() == QtCore.Qt.Key.Key_Left.value:
                self.slewCCW = True
            if event.key() == QtCore.Qt.Key.Key_Right.value:
                self.slewCW = True
            if event.key() == QtCore.Qt.Key.Key_Up.value:
                 self.tiltUp = True
            if event.key() == QtCore.Qt.Key.Key_Down.value:
                 self.tiltDown = True
            if event.text().upper() == "A":
                self.left = True
            if event.text().upper() == "D":
                self.right = True
            if event.text().upper() == "W":
                self.fwd = True
            if event.text().upper() == "S":
                self.bwd = True
            if event.text().upper() == "E":
                self.up = True
            if event.text().upper() == "Q":
                self.down = True


    def keyreleaseevent(self, event):
        if event.text().upper() == "W":
            self.fwd = False
        if event.text().upper() == "S":
            self.bwd = False
        if event.text().upper() == "D":
            self.right = False
        if event.text().upper() == "A":
            self.left = False
        if event.key() == QtCore.Qt.Key.Key_Right.value:
            self.slewCW = False
        if event.key() == QtCore.Qt.Key.Key_Left.value:
            self.slewCCW = False
        if event.key() == QtCore.Qt.Key.Key_Up.value:
            self.tiltUp = False
        if event.key() == QtCore.Qt.Key.Key_Down.value:
            self.tiltDown = False
        if event.text().upper() == "E":
            self.up = False
        if event.text().upper() == "Q":
            self.down = False


    def onupdate(self,deltaTime):
        self.positionDelta = glm.vec3(0, 0, 0)


        for ent, (trans, camera,) in self.scene.get_components(TransformComponent, CameraComponent):
            trans: TransformComponent

            if self.fwd:
                self.positionDelta += trans.Forward
            if self.bwd:
                self.positionDelta += - trans.Forward
            if self.right:
                self.positionDelta += trans.Right
            if self.left:
                self.positionDelta +=  - trans.Right
            if self.slewCW:
                trans.yaw += 1.0
            if self.slewCCW:
                trans.yaw -= 1.0
            if self.tiltUp:
                trans.pitch += 1.0
            if self.tiltDown:
                trans.pitch -= 1.0
            if self.up:
                self.positionDelta += glm.vec3(0,1,0)
            if self.down:
                self.positionDelta += - glm.vec3(0,1,0)

            self.direction = glm.vec3(0,0,0)
            self.direction.x = cos(glm.radians(trans.yaw)) * cos(glm.radians(trans.pitch))
            self.direction.y = sin(glm.radians(trans.pitch))
            self.direction.z = sin(glm.radians(trans.yaw)) * cos(glm.radians(trans.pitch))

            trans.Right = glm.normalize(glm.cross(trans.Forward, glm.vec3(0.0, 1.0, 0.0)))
            trans.Up = glm.normalize(glm.cross(trans.Right, trans.Forward))
            trans.Forward = glm.normalize(self.direction)

            trans.Translation += self.speed * deltaTime * self.positionDelta













