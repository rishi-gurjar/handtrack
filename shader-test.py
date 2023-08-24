import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Initialize pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Define GLSL shaders
vertex_shader = """
#version 330
in vec4 position;
void main()
{
    gl_Position = position;
}
"""

fragment_shader = """
#version 300 es
precision mediump float;
out vec4 fragColor;
uniform vec2 u_resolution;
uniform float u_time;
#define PI 3.141592653589793
#define cx_div(a, b) vec2(((a.x*b.x+a.y*b.y)/(b.x*b.x+b.y*b.y)),((a.y*b.x-a.x*b.y)/(b.x*b.x+b.y*b.y)))
vec2 as_polar(vec2 z) {
  return vec2(
    length(z),
    atan(z.y, z.x)
  );
}
vec2 cx_log(vec2 a) {
    vec2 polar = as_polar(a);
    float rpart = polar.x;
    float ipart = polar.y;
    if (ipart > PI) ipart=ipart-(2.0*PI);
    return vec2(log(rpart),ipart);
}
vec3 palette( in float t, in vec3 a, in vec3 b, in vec3 c, in vec3 d ) {
    return a + b*cos( 0.38*2.*PI*(c*t+d) );
}
void main() {
  vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution.xy) / min(u_resolution.y, u_resolution.x);
  vec2 z = uv;
  float angle = sin(u_time/5.) * 2. * PI;
  float length = .2;
  float c = cos(angle);
  float s = sin(angle);
  vec2 p = vec2( s*length, c*length);
  vec2 q = vec2( s*-length, c*-length );
  vec2 division = cx_div((z - p), (z - q));
  vec2 log_p_over_q = cx_log(division);
  float imaginary = log_p_over_q.y / PI;
  vec3 col = palette( imaginary, vec3(0.50,.52,0.53), vec3(.46,.32,.35), vec3(.82,.84,.65), vec3(0.53,0.23,0.22));
  fragColor = vec4(col, 1.0);
}
"""

# Compile shaders and program
shader_program = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

# Define a simple square
square = [
    -1.0, -1.0, 0,
    1.0, -1.0, 0,
    1.0, 1.0, 0,
    -1.0, 1.0, 0,
]
square = [float(x) for x in square]

# Create a Vertex Buffer Object (VBO)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(square) * 4, (GLfloat * len(square))(*square), GL_STATIC_DRAW)

# Main loop
start_time = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Use the shader program
    glUseProgram(shader_program)

    # Set the resolution and time uniforms
    glUniform2f(glGetUniformLocation(shader_program, "u_resolution"), display[0], display[1])
    glUniform1f(glGetUniformLocation(shader_program, "u_time"), (pygame.time.get_ticks() - start_time) / 1000.0)

    # Bind the VBO
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # Enable the position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    # Draw the square
    glDrawArrays(GL_QUADS, 0, 4)

    # Swap buffers
    pygame.display.flip()
    pygame.time.wait(10)
