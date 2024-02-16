#version 330

/*--------------------------------------------------------------------*/
#if defined VERTEX_SHADER
/*--------------------------------------------------------------------*/

uniform mat4 projection;

in vec2 in_vert;

void main() {
    gl_Position = projection * vec4(in_vert, 0.0, 1.0);
}

/*--------------------------------------------------------------------*/
#elif defined FRAGMENT_SHADER
/*--------------------------------------------------------------------*/

out vec4 fragColor;
uniform vec4 line_colour;

void main() {
    fragColor = line_colour;
}

#endif
