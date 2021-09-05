#shader vertex
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 Normal;
layout(location = 2) in vec4 color;
layout(location = 3) in float EntityID;

uniform mat4 u_Projection;
uniform mat4 u_View;
uniform mat4 u_Model;
uniform vec3 u_lightPos;


out vec4 v_Color;
out vec3 v_FragPos;
out vec3 v_Normal;
out vec3 v_lightPos;
out vec3 textureCoords;
flat out float v_EntityID;

void main() {

//    gl_Position = u_ViewProjection *  vec4(position, 1.0);
    gl_Position = u_Projection * u_View *  vec4(position, 1.0);
    v_FragPos = vec3(u_Model * vec4(position, 1.0));
    textureCoords = position;
    v_Color = color;
    v_EntityID = EntityID;
    v_Normal = Normal;
    v_lightPos = u_lightPos;



}
    #shader fragment
    #version 330 core
layout(location = 0) out vec4 color;
layout(location = 1) out int color2;

in vec3 textureCoords;
in vec4 v_Color;
in vec3 v_Normal;
in vec3 v_FragPos;
in vec3 v_lightPos;
flat in float v_EntityID;

uniform samplerCube cubeMap;

void main() {

    int EntityID = int(v_EntityID);
    // ambient
    float ambientStrength = 0.3;
    vec3 ambient = ambientStrength * vec3(1,1,1);

    //diffuse
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = normalize(v_lightPos - v_FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * vec3(1,1,1);


    color = v_Color;
//    color = vec4((ambient + diffuse),1) * texture(cubeMap, textureCoords);
//    color *= vec4((ambient + diffuse),1);
        color *= texture(cubeMap, textureCoords);
    color *= vec4((ambient + diffuse),1);
    color2 = EntityID;
}
