#shader vertex
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec4 color;
layout(location = 2) in vec2 TexCoord;
layout(location = 3) in float TexID;
layout(location = 4) in float EntityID;

uniform mat4 u_ViewProjection;
uniform mat4 u_Transform;
uniform int indexio;
out vec2 v_TexCoord;
out vec4 v_Color;
flat out float v_TexID;
flat out float v_test;




void main() {

    gl_Position = u_ViewProjection * u_Transform *  vec4(position, 1.0);
    v_TexCoord = TexCoord;

    v_Color = color;
    v_TexID = TexID;
    v_test = EntityID;

}
    #shader fragment
    #version 330 core
layout(location = 0) out vec4 color;
layout(location = 1) out int color2;
in vec2 v_TexCoord;
in vec4 v_Color;
flat in float v_test;
flat in float v_TexID;


uniform vec4 u_Color;
uniform sampler2D u_Texture;
uniform sampler2D u_Textures[32];

void main() {
    int test = int(v_test);
    int index = int(v_TexID);
    vec4 texColor = v_Color;
    texColor *= texture(u_Textures[index], v_TexCoord);
    color = texColor;
    color2 = test;
}
