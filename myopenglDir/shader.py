from OpenGL.GL import *


class Shader():
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.locationCache = {}

        vertexShader, fragmentShader = self.parseshader(self.filepath)
        self.m_RenderID = self.CreateShader(vertexShader, fragmentShader)
        glUseProgram(self.m_RenderID)

    def Bind(self):
        glUseProgram(self.m_RenderID)

    def UnBind(self):
        glUseProgram(0)

    def SetUniform1i(self, name, v0):
        location = self.GetUniformlocation(name)
        glUniform1i(location, v0)

    def SetUniform1iv(self, name, v0):
        location = self.GetUniformlocation(name)
        glUniform1iv(location, len(v0), v0)

    def SetUniform1f(self, name, v0):
        location = self.GetUniformlocation(name)
        glUniform1f(location, v0)

    def SetUniform3f(self, name, v0, v1, v2):
        location = self.GetUniformlocation(name)
        glUniform3f(location, v0, v1, v2)

    def SetUniform3fv(self, name, value):
        location = self.GetUniformlocation(name)
        glUniform3fv(location,1,value)

    def SetUniform4f(self, name, v0, v1, v2, v3):
        location = self.GetUniformlocation(name)
        glUniform4f(location, v0, v1, v2, v3)

    def SetUniformMath4f(self, name, matrix):
        location = self.GetUniformlocation(name)
        glUniformMatrix4fv(location, 1, GL_TRUE, matrix)

    def GetUniformlocation(self, name):
        if name in self.locationCache:
            return self.locationCache[name]
        else:
            location = glGetUniformLocation(self.m_RenderID, name)
            self.locationCache[name] = location
        return location

    def CreateShader(self, vertexShader, fragmentShader):
        program = glCreateProgram()
        vs = self.CompileShader(GL_VERTEX_SHADER, vertexShader)
        fs = self.CompileShader(GL_FRAGMENT_SHADER, fragmentShader)
        glAttachShader(program, vs)
        glAttachShader(program, fs)
        glLinkProgram(program)
        glValidateProgram(program)
        glDeleteShader(vs)
        glDeleteShader(fs)
        return program

    def CompileShader(self, type, source):
        id = glCreateShader(type)
        glShaderSource(id, source)
        glCompileShader(id)

        result = glGetShaderiv(id, GL_COMPILE_STATUS)
        if not result:
            length = glGetShaderiv(id, GL_INFO_LOG_LENGTH)
            message = glGetShaderInfoLog(id)

            print(f"Failed to compile shader \n"
                  f"{type}\n"
                  f"{message}")
        return id

    def parseshader(self, filepath):
        class ShaderType():
            NONE = -1
            VERTEX = 0
            FRAGMENT = 1

        ss = [""] * 2
        type = ShaderType.NONE
        with open(filepath) as f:
            lines = f.readlines()
            for line in lines:
                if "shader" in line:
                    if "vertex" in line:
                        type = ShaderType.VERTEX
                    elif "fragment" in line:
                        type = ShaderType.FRAGMENT
                else:
                    ss[type] += line
            return ss
