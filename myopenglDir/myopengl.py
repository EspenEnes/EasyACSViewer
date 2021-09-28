import datetime

import PyQt6
from OpenGL.GL import *
from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QMouseEvent, QContextMenuEvent, QAction
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QWidget, QMenu

from ECS.components import *
from ECS.scene import Scene, TagComponent, RenderComponent
from ECS.sceneCameraController import CameraController
from CostumFunctions.costumFunctions import SkyboxCube, Quad2d
from ECS.functions import creatEcsEntitys
from myopenglDir.framebuffer import Framebuffer
from myopenglDir.offlinerenderer import OfflineRenderer


class CostumSignals(QObject):
    initializeGL_Done = pyqtSignal(bool)
    EcsScene_Created = pyqtSignal(object)
    Entity_clicked = pyqtSignal(str)
    Data = pyqtSignal(dict)
    aaa = pyqtSignal(bool)



class MyOPENGL(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setMouseTracking(True)
        self.signals = CostumSignals()
        self.signals.Data.connect(self.ECSEntitys)

        timer = QtCore.QTimer(self)
        timer.setInterval(20)  # period, in milliseconds
        timer.timeout.connect(self.update)
        timer.start()

        self.timer2 = QtCore.QTimer(self)
        self.timer2.setInterval(100)  # period, in milliseconds
        self.timer2.timeout.connect(self.update2)



        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

        self.mouseX = None
        self.mouseY = None
        self.HoveredEntity = None
        self.SelectedEntity =  -1
        self.previusdt = datetime.datetime.now()

    def update2(self):
        if self.SelectedEntity is None:
            return

        if self.SelectedEntity >= 0:

            tag = self.scene.scene.component_for_entity(self.SelectedEntity , TagComponent)
            box: AcsBoxComponent = self.scene.scene.component_for_entity(self.SelectedEntity , AcsBoxComponent)
            data = f"{tag.FriendlyName}\n" \
                   f"Xmax: {box.Xmax}, Xmin: {box.Xmin}\n" \
                   f"Ymax: {box.Ymax}, Ymin: {box.Ymin}\n" \
                   f"Zmax: {box.Zmax}, Zmin: {box.Zmin}"
            self.signals.Entity_clicked.emit(data)

            self.timer2.start()
        else:
            self.signals.Entity_clicked.emit("")




    def event(self, e: QtCore.QEvent) -> bool:
        if type(e) == PyQt6.QtGui.QMouseEvent:
            e:PyQt6.QtGui.QMouseEvent
            self.mouseX = e.position().x()
            self.mouseY = e.position().y()

            if e.button() == Qt.MouseButton.LeftButton:
                self.SelectedEntity = self.HoveredEntity
                self.update2()
                return True

        if type(e) == PyQt6.QtGui.QContextMenuEvent:
            e :  PyQt6.QtGui.QContextMenuEvent
            self.contextMenu(e.globalPos())
            return True

        if e.type() == QtCore.QEvent.Type.KeyPress:
            self.CameraController.keypressevent(e)

            return True
        elif e.type() == QtCore.QEvent.Type.KeyRelease:
            self.CameraController.keyreleaseevent(e)
            return True
        return super(MyOPENGL, self).event(e)

    
    def contextMenu(self, pos):
        menu = QMenu()
        if self.HoveredEntity >= 0:
            tag = self.scene.scene.component_for_entity(self.HoveredEntity, TagComponent)

            actionHide = QAction(self)
            actionHide.triggered.connect(lambda: self.hideEntity(self.HoveredEntity))
            actionHide.setText(f"Hide {tag.FriendlyName}")
            menu.addAction(actionHide)
            menu.exec(pos)

    def hideEntity(self, entity):
        ren = self.scene.scene.component_for_entity(entity, RenderComponent)
        ren.Visible = False

    def ECSEntitys(self, data):

        creatEcsEntitys(data, self.scene)





        self.signals.EcsScene_Created.emit(self.scene)

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)

        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.FBO = Framebuffer(2, 1, self.width(), self.height())



        self.offlinerenderer = OfflineRenderer()
        self.scene = Scene()
        self.CameraController = CameraController(self.scene)

        camera = self.scene.CreateEntity("Camera")
        camera.AddComponent(CameraComponent())
        trans = camera.GetComponent(TransformComponent)
        trans.yaw = 0
        trans.pitch = -30
        trans.Translation = (-120, 7, 100)

        SkyBox = self.scene.CreateEntity("Skybox")
        SkyBox.AddComponent(MeshComponent())

        mesh: MeshComponent = SkyBox.GetComponent(MeshComponent)
        mesh.Vertesies = SkyboxCube()
        mesh.Indesies = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                         24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

        floor = self.scene.CreateEntity("Floor")
        floor.AddComponent(MeshComponent())
        floor.AddComponent(RenderComponent())
        mesh: MeshComponent = floor.GetComponent(MeshComponent)

        Vertecies = list()
        Indesies = list()
        idx = 0
        for y in range(0, 30):
            for x in range(0, 30):
                color = [2, 2, 2, 1]
                if (x + y) % 2 == 0:
                    color = [.5, .5, .5, 1]

                v, i = Quad2d(x - 115, 0, y + 85, (1, 1), 0, color)
                Vertecies += v
                Indesies += [x + idx for x in i]
                a = Indesies.copy()
                a.sort()
                idx = a[-1] + 1
        mesh.Vertesies = np.array(Vertecies, dtype=np.float32)
        mesh.Indesies = Indesies

        # mesh.Vertesies, mesh.Indesies = Quad2d(-100,0,100,(500,500),0,(.8,.6,.4,1),pitch=90)
        #
        ren: RenderComponent = floor.GetComponent(RenderComponent)
        ren.Visible = True

        self.signals.initializeGL_Done.emit(True)


    def resizeGL(self, width, height):
        self.FBO.Resize(width, height)
        self.scene.OnViewportResize(width, height)

    def paintGL(self):
        self.dt = datetime.datetime.now() -  self.previusdt
        self.previusdt = datetime.datetime.now()

        self.CameraController.onupdate(self.dt.microseconds / 1000)

        self.FBO.Bind()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.scene.scene.process()
        if self.mouseX is not None :
            self.HoveredEntity = self.FBO.ReadEntity(self.mouseX, self.height() - self.mouseY)


        glBindFramebuffer(GL_FRAMEBUFFER, self.defaultFramebufferObject())
        glDisable(GL_DEPTH_TEST)
        glBindTextureUnit(0, self.FBO.m_ColorAttachments[0])

        self.offlinerenderer.BeginScene()
        self.offlinerenderer.plainBox()
        self.offlinerenderer.EndScene()
