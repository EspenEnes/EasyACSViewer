import numpy as np
from OpenGL.GL import *


class Framebuffer():
    def __init__(self, nColorAtachments, nDepthAtachments, width, height):
        self.m_RenderID = None
        self.width = width
        self.height = height
        self.nColorAtachments = nColorAtachments
        self.nDepthAtachments = nDepthAtachments
        self.invalidate()

    def invalidate(self):
        if self.m_RenderID is not None:
            glDeleteFramebuffers(1, np.array(self.m_RenderID, dtype=np.int))
            glDeleteTextures(self.nColorAtachments, np.array(self.m_ColorAttachments, dtype=np.int))
            glDeleteTextures(self.nDepthAtachments, np.array(self.m_DepthAttachments, dtype=np.int))

            self.m_ColorAttachments = np.empty(self.nColorAtachments, dtype=np.uint32)
            self.m_DepthAttachment = None

        self.m_RenderID = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.m_RenderID)

        self.m_ColorAttachments = self.CreateTextures(self.nColorAtachments)

        for index, Attachment in enumerate(self.m_ColorAttachments):
            self.BindTexture(Attachment)
            self.AttachColorTexture(Attachment, index)

        self.m_DepthAttachments = self.CreateTextures(self.nDepthAtachments)

        for index, Attachment in enumerate(self.m_DepthAttachments):
            self.BindTexture(Attachment)
            self.AttachDepthTexture(Attachment)

        if True:
            a_type = GLenum * 2
            drawingBuffers = a_type(
                GL_COLOR_ATTACHMENT0,
                GL_COLOR_ATTACHMENT1,
            )
            glDrawBuffers(self.nColorAtachments, drawingBuffers)



        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def CreateTextures(self, count):
        outID = np.empty(count, dtype=np.uint32)
        glCreateTextures(GL_TEXTURE_2D, count, outID)
        return outID

    def BindTexture(self, id):
        glBindTexture(GL_TEXTURE_2D, id)

    def AttachColorTexture(self, id, index):
        if index == 0:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + index, GL_TEXTURE_2D, id, 0)

        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_R32I, self.width, self.height, 0, GL_RED_INTEGER, GL_UNSIGNED_BYTE, None)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + index, GL_TEXTURE_2D, id, 0)

    def AttachDepthTexture(self, id):
        glTexStorage2D(GL_TEXTURE_2D, 1, GL_DEPTH24_STENCIL8, self.width, self.height)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D, id, 0)

    def ReadEntity(self, x, y):



        glReadBuffer(GL_COLOR_ATTACHMENT1)
        pixelData = glReadPixels(x, y, 1, 1,
                                 GL_RED_INTEGER,
                                 GL_INT)

        return pixelData[0][0]

    def Bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.m_RenderID)

    def UnBind(self, ID=0):

        glBindFramebuffer(GL_FRAMEBUFFER, ID)


    def Resize(self, width, height):
        self.width = width
        self.height = height

        self.invalidate()
