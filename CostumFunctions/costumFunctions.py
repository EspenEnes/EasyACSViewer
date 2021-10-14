from ECS.components import *
from collections import namedtuple
Color = namedtuple("Color", ["R", "G", "B", "A"])


ipv4 = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def ACSCube(Xmin=-1,Xmax=1,Ymin=-1,Ymax=1,Zmin=-1,Zmax=1,color=(5,5,5,5), EntityId=-1):

    Positions =          [Xmin, Ymax, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,0,0,-1,color[0], color[1], color[2], color[3],

                          Xmin, Ymin, Zmax,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmin,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmax,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,-1,0,0,color[0], color[1], color[2], color[3],

                          Xmax, Ymin, Zmin,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmax,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmin,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,1,0,0,color[0], color[1], color[2], color[3],

                          Xmin, Ymin, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,0,0,1,color[0], color[1], color[2], color[3],

                          Xmin, Ymax, Zmin,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmin,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmax,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,0,-1,0,color[0], color[1], color[2], color[3],

                          Xmin, Ymin, Zmin,0,1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,0,1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,0,1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmax,0,1,0,color[0], color[1], color[2], color[3]]
    #Add inn Color Vector
    # Vertecies = [x for y in (Positions[i:i + 6] + color[0 , color[1*, color[2 , color[3(i < len(Positions) - 4) for i in range(0, len(Positions), 4)) for x in y]
    # Add inn Entity Vector
    Vertecies = [x for y in
                 (Positions[i:i + 10] + [EntityId] * (i < len(Positions) - 1) for i in range(0, len(Positions), 10)) for x
                 in y]



    return np.array(Vertecies, dtype=np.float32)



def SkyboxCube():
    SIZE = 500.0

    Vertecies = np.array([-SIZE, SIZE, -SIZE,
                          -SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,
                          SIZE, SIZE, -SIZE,
                          -SIZE, SIZE, -SIZE,

                          -SIZE, -SIZE, SIZE,
                          -SIZE, -SIZE, -SIZE,
                          -SIZE, SIZE, -SIZE,
                          -SIZE, SIZE, -SIZE,
                          -SIZE, SIZE, SIZE,
                          -SIZE, -SIZE, SIZE,

                          SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,

                          -SIZE, -SIZE, SIZE,
                          -SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, -SIZE, SIZE,
                          -SIZE, -SIZE, SIZE,

                          -SIZE, SIZE, -SIZE,
                          SIZE, SIZE, -SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          -SIZE, SIZE, SIZE,
                          -SIZE, SIZE, -SIZE,

                          -SIZE, -SIZE, -SIZE,
                          -SIZE, -SIZE, SIZE,
                          SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,
                          -SIZE, -SIZE, SIZE,
                          SIZE, -SIZE, SIZE], dtype=np.float32)

    return np.array(Vertecies, dtype=np.float32)


def Quad2d(x, y, z, size, TexID=0, color=None, roll=0.0, pitch=0.0, entityID=-1):
    width, hight = size

    transformPos = glm.translate(glm.mat4(), glm.vec3(x, y, z))
    transformRoll = glm.rotate(glm.mat4(), glm.radians(roll), glm.vec3(0, 0, 1))
    transformPitch = glm.rotate(glm.mat4(), glm.radians(pitch), glm.vec3(1, 0, 0))
    transform = transformPos * transformRoll * transformPitch
    position = glm.vec4()

    # np.array([entityID],dtype=np.uintc)

    if color is None:
        r, g, b, a = (1, 1, 1, 1)
    else:
        r, g, b, a = color

    # V1
    position.x = - width / 2
    position.z = - hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x, y, 50]
    color = [r, g, b, a]
    normals = [0,1,0]
    TextureCorr = [0, 0]
    TextureID = [TexID]
    v1 = positions + normals  + color + [entityID]

    # v2
    position.x = width / 2
    position.z = - hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x + width, y, 50]
    color = [r, g, b, a]
    normals = [0,1,0]
    TextureCorr = [1.0, 0.0]
    TextureID = [TexID]
    v2 = positions + normals + color + [entityID]

    # v3
    position.x = width / 2
    position.z = hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x + width, y + hight, 50]
    color = [r, g, b, a]
    normals = [0, 1, 0]
    TextureCorr = [1.0, 1.0]
    TextureID = [TexID]
    v3 = positions + normals + color + [entityID]

    # v4
    position.x = - width / 2
    position.z = hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x, y + hight, 50]
    color = [r, g, b, a]
    normals = [0, 1, 0]
    TextureCorr = [0.0, 1.0]
    TextureID = [TexID]
    v4 = positions + normals + color + [entityID]

    Vertecies = v1 + v2 + v3 + v4
    Indesies =  [0, 1, 2, 2, 3, 0]

    return Vertecies, Indesies


if __name__ == '__main__':
    cube = ACSCubeUDP()
    vert, norm, text = cube.buildVertices()