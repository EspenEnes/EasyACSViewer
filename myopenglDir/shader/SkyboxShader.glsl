#shader vertex
#version 330 core

in vec3 position;
out vec3 textureCoords;

//uniform mat4 projectionMatrix;
//uniform mat4 viewMatrix;
uniform mat4 u_ViewProjection;

void main(void){

    gl_Position = u_ViewProjection * vec4(position, 1.0);
    textureCoords = position;

}
    #shader fragment
    #version 330 core
in vec3 textureCoords;
layout(location = 0) out vec4 out_Color;
layout(location = 1) out int out_Color2;

uniform samplerCube cubeMap;

void main(void){
    out_Color = texture(cubeMap, textureCoords);
    out_Color2 = -1;

}
