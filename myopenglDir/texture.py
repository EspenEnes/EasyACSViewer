import os

import cv2
import numpy as np
from OpenGL.GL import *


class Texture():
    def __init__(self, path=None, repeat=False):
        if path is not None:
            self.filepath = path

            self.m_LocalBuffer = cv2.flip(cv2.imread(self.filepath, cv2.IMREAD_UNCHANGED), 0)
            self.Height, self.w_Width, self.m_BPP = self.m_LocalBuffer.shape

            if self.m_BPP == 3:
                self.m_LocalBuffer = cv2.cvtColor(self.m_LocalBuffer, cv2.COLOR_RGB2RGBA)
                self.Height, self.w_Width, self.m_BPP = self.m_LocalBuffer.shape

        else:
            self.Height, self.w_Width, self.m_BPP = 1, 1, 4
            self.m_LocalBuffer = np.array([[[255, 255, 255, 255]]], dtype=np.float32)

        glEnable(GL_TEXTURE_2D)

        self.m_RenderID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_RenderID)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        if repeat:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)


        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.w_Width, self.Height, 0, GL_BGRA, GL_UNSIGNED_BYTE,
                     self.m_LocalBuffer)

        glBindTexture(GL_TEXTURE_2D, 0)

        # if  self.m_LocalBuffer != None:
        #     self.m_LocalBuffer = None

    def cv2array(self, im):
        h, w, c = im.shape
        a = np.fromstring(
            im.tostring(),
            dtype=im.dtype,
            count=w * h * c)
        a.shape = (h, w, c)
        return a

    def Bind(self, slot=0):
        # glActiveTexture(GL_TEXTURE0 + slot)
        # glBindTexture(GL_TEXTURE_2D, self.m_RenderID)

        # same as
        glBindTextureUnit(slot, self.m_RenderID)

    def UnBind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    @property
    def GetWidth(self):
        return self.w_Width

    @property
    def GetHight(self):
        return self.Height



class CubeMap:
    def __init__(self, path=None):
        self.filepath = path

        self.m_RenderID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.m_RenderID)

        if path is not None:
            for num, file in enumerate(os.listdir(path)):

                self.m_LocalBuffer = cv2.flip(cv2.imread(self.filepath + "/" + file, cv2.IMREAD_UNCHANGED), 1)
                self.Height, self.w_Width, self.m_BPP = self.m_LocalBuffer.shape

                if self.m_BPP == 3:
                    self.m_LocalBuffer = cv2.cvtColor(self.m_LocalBuffer, cv2.COLOR_RGB2RGBA)
                    self.Height, self.w_Width, self.m_BPP = self.m_LocalBuffer.shape

                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + num, 0, GL_RGBA, self.w_Width, self.Height, 0, GL_BGRA,
                             GL_UNSIGNED_BYTE,
                             self.m_LocalBuffer)
        else:
            self.Height, self.w_Width, self.m_BPP = 1, 1, 4
            self.m_LocalBuffer = np.array([[[255, 255, 255, 255]]], dtype=np.float32)
            for num in range(0, 6):
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + num, 0, GL_RGBA, self.w_Width, self.Height, 0, GL_BGRA,
                             GL_UNSIGNED_BYTE,
                             self.m_LocalBuffer)



        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def Bind(self, slot=0):
        glBindTextureUnit(slot, self.m_RenderID)

    def UnBind(self):
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    @property
    def GetWidth(self):
        return self.w_Width

    @property
    def GetHight(self):
        return self.Height


if __name__ == '__main__':
    texture = Texture("res/textures/Superman.png")
    cv2.imshow('Original image', texture.m_LocalBuffer)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
