from math import pi, cos, sin

"""
SbGA.Jib.Line1.Position.XA	REAL	0.000000e+000	97.73	 Base point X-coordinate	
SbGA.Jib.Line1.Position.YA	REAL	0.000000e+000	96.6	 Base point Y-coordinate	
SbGA.Jib.Line1.Position.ZA	REAL	0.000000e+000	9.2	 Base point Z-coordinate	
SbGA.Jib.Line1.Position.Slew	REAL	0.000000e+000	-0.7853981	 Slew Angle (Rad)	
SbGA.Jib.Line1.Position.Tilt	REAL	0.000000e+000	1.570796	 Tilt Angle (Rad)	
SbGA.Jib.Line1.Position.Length	REAL	0.000000e+000	3.0	 Length	
SbGA.Jib.Line1.Position.Width	REAL	0.000000e+000	0.3	 Width ( Radius)	
"""


class ACSCubeUDP():
    def __init__(self, Xmin=95,Xmax=105,Ymin=95,Ymax=105,Zmin=0,Zmax=100,color=(5,5,5,5), EntityId=-1):
        self.BaseXpos = ((Xmax - Xmin) / 2) + Xmin
        self.BaseYpos = ((Ymax - Ymin) / 2) + Ymin
        self.BaseZpos = ((Zmax - Zmin) / 2) + Zmin

        self.XpLength = Xmax - self.BaseXpos
        self.XnLength = self.BaseXpos - Xmin
        self.YpLength = Ymax - self.BaseYpos
        self.YnLength = self.BaseYpos - Ymin
        self.ZpLength = Zmax - self.BaseZpos
        self.ZnLength = self.BaseZpos - Zmin

        self.sectorcounts = 4

    def getUnitBaseVertices(self):
        unitCircleVertices = list()
        sectorStep = 2 * pi / self.sectorcounts

        for sector in range(0, self.sectorcounts + 1):
            sectorAngle = sector * sectorStep

            unitCircleVertices.append(float(f"{cos(sectorAngle): .3f}"))
            unitCircleVertices.append(float(f"{sin(sectorAngle): .3f}"))
            unitCircleVertices.append(0.0)
        return unitCircleVertices

    def buildVertices(self):
            unitVertices = self.getUnitBaseVertices()
            vertices = list()
            normals = list()
            textCoords = list()

            # put side vertices to arrays
            for i in range(0, 2):
                h = self.BaseZpos - (self.height / 2) + i * (self.height)
                t = 1.0 - i
                k = 0

                for j in (range(0, self.sectorcounts + 1)):
                    ux = unitVertices[k]
                    uy = unitVertices[k + 1]
                    uz = unitVertices[k + 2]

                    # position vector
                    vertices.append(ux * (self.width / 2) + self.BaseXpos)
                    vertices.append(uy * (self.depth / 2) + self.BaseYpos)
                    vertices.append(h)

                    # normal vector
                    normals.append(ux)
                    normals.append(uy)
                    normals.append(uz)

                    # texture coordinate
                    textCoords.append(float(j) / self.sectorcounts)
                    textCoords.append(t)
                    k += 3

            self._baseStartIndex = int(len(vertices) / 3)
            self._topStartIndex = self._baseStartIndex + self.sectorcounts + 1

            # put base and top vertices to arrays
            for i in range(0, 2):
                 h = self.BaseZpos - (self.height / 2) + i * self.height
                 nz = -1 + i * 2

                 k = 0
                 for j in range(0, self.sectorcounts):
                     ux = unitVertices[k]
                     uy = unitVertices[k + 1]

                     # position vector
                     vertices.append(ux * (self.width / 2) + self.BaseXpos)
                     vertices.append(uy * (self.depth / 2) + self.BaseYpos)
                     vertices.append(h)

                     # normal vector
                     normals.append(0.0)
                     normals.append(0.0)
                     normals.append(nz)

                     # texture coordinate
                     textCoords.append(-ux * 0.5 + 0.5)
                     textCoords.append(-uy * 0.5 + 0.5)
                     k += 3
            return vertices, normals, textCoords

    @property
    def width(self):
        return (self.XnLength + self.XpLength)

    @property
    def depth(self):
        return (self.YnLength + self.YpLength)

    @property
    def height(self):
        return (self.ZnLength + self.ZpLength)






class Cylinder():
    def __init__(self, radius: float = 1.0, height: float = 1.0, sectorcounts: int = 8):
        self.sectorcounts = sectorcounts
        self.radius = radius
        self.height = height

        self.build()

    def build(self):
        self._vertices, self._normals, self._textCoords = self.buildVertices()
        self._indices = self.buildIndices()


    def getUnitCircleVertices(self):
        unitCircleVertices = list()
        sectorStep = 2 * pi / self.sectorcounts

        for sector in range(0, self.sectorcounts + 1):
            sectorAngle = sector * sectorStep
            unitCircleVertices.append(cos(sectorAngle))
            unitCircleVertices.append(sin(sectorAngle))
            unitCircleVertices.append(0.0)
        return unitCircleVertices


    def buildVertices(self):
        unitVertices = self.getUnitCircleVertices()
        vertices = list()
        normals = list()
        textCoords = list()

        # put side vertices to arrays
        for i in range(0, 2):
            h = -self.height / 2.0 + i * self.height
            t = 1.0 - i

            k = 0
            for j in (range(0, self.sectorcounts + 1)):
                ux = float(unitVertices[k])
                uy = unitVertices[k + 1]
                uz = unitVertices[k + 2]

                # position vector
                vertices.append(ux * self.radius)
                vertices.append(uy * self.radius)
                vertices.append(h)

                # normal vector
                normals.append(ux)
                normals.append(uy)
                normals.append(uz)

                # texture coordinate
                textCoords.append(float(j) / self.sectorcounts)
                textCoords.append(t)
                k += 3

        # the starting index for the base / top surface
        self._baseCenterIndex = int(len(vertices) / 3)
        self._topCenterIndex = self._baseCenterIndex + self.sectorcounts + 1

        # put base and top vertices to arrays
        for i in range(0, 2):
            h = -self.height / 2.0 + i * self.height
            nz = -1 + i * 2

            #center point
            vertices.append(0.0)
            vertices.append(0.0)
            vertices.append(h)

            normals.append(0.0)
            normals.append(0.0)
            normals.append(nz)

            textCoords.append(0.5)
            textCoords.append(0.5)

            k = 0
            for j in range(0, self.sectorcounts):
                ux = unitVertices[k]
                uy = unitVertices[k + 1]

                #position vector
                vertices.append(ux * self.radius)
                vertices.append(uy * self.radius)
                vertices.append(h)

                #normal vector
                normals.append(0.0)
                normals.append(0.0)
                normals.append(nz)

                #texture coordinate
                textCoords.append(-ux * 0.5 + 0.5)
                textCoords.append(-uy * 0.5 + 0.5)
                k += 3
        return vertices, normals, textCoords

    def buildIndices(self):
        indices = list()

        k1 = 0
        k2 = self.sectorcounts + 1

        #indices for the side surface
        for i in range(0, self.sectorcounts):
            indices.append(k1)
            indices.append(k1 + 1)
            indices.append(k2)

            indices.append(k2)
            indices.append(k1 + 1)
            indices.append(k2 + 1)
            k1 += 1
            k2 += 1

        #indices for the base surface
        k = self._baseCenterIndex + 1
        for i in range(0, self.sectorcounts):

            if i < self.sectorcounts - 1:
                indices.append(self._baseCenterIndex)
                indices.append(k + 1)
                indices.append(k)
            else:
                indices.append(self._baseCenterIndex)
                indices.append(self._baseCenterIndex + 1)
                indices.append(k)
            k += 1

        #indices for the top surface
        k = self._topCenterIndex + 1
        for i in range(0, self.sectorcounts):

            if i < self.sectorcounts - 1:
                indices.append(self._topCenterIndex)
                indices.append(k)
                indices.append(k + 1)
            else:
                indices.append(self._topCenterIndex)
                indices.append(k)
                indices.append(self._topCenterIndex + 1)
            k += 1
        return indices

    @property
    def sectorcounts(self):
        return self._sectorcounts

    @sectorcounts.setter
    def sectorcounts(self, value):
        self._sectorcounts = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def vertices(self):
        return self._vertices

    @property
    def normals(self):
        return self._normals

    @property
    def textCoords(self):
        return self._textCoords

    @property
    def indices(self):
        return self._indices

    def costumvertecies(self, color, entityId):
        """returns vertecies in Position, normal, color, ID """
        vertices = list()
        verticeSets = list()
        normalSets = list()
        textcordSets = list()
        for i in range(0, len(self.vertices), 3):
            verticeSets.append(self.vertices[i: i+3])

        for i in range(0, len(self.normals), 3):
            normalSets.append(self.normals[i: i+3])

        for i in range(0, len(self.textCoords), 2):
            textcordSets.append(self.textCoords[i: i+2])

        for x in range(0, len(verticeSets)):
            vertices += verticeSets[x]
            vertices += normalSets[x]
            #vertices += textcordSets[x]
            vertices += color
            vertices += [-1]

        return vertices

if __name__ == '__main__':
    cyliner = Cylinder()



