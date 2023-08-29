import glfw
from OpenGL.GL import *

# Initialize GLFW
if not glfw.init():
    print("Failed to initialize GLFW")
    exit()

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(640, 480, "GLSL Version", None, None)
if not window:
    glfw.terminate()
    print("Failed to create GLFW window")
    exit()

# Make the window's context current
glfw.make_context_current(window)

# Print GLSL version
print(glGetString(GL_SHADING_LANGUAGE_VERSION))

# Terminate GLFW
glfw.terminate()
