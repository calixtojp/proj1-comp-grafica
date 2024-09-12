#importação de bibliotecas
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

# Iniciando janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
window = glfw.create_window(700, 700, "Projeto", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec3 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,1.0);
        }
        """

fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

# Request a program and shader slots from GPU
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
# Make program the default program
glUseProgram(program)

# preparando espaço para 24 vértices usando 3 coordenadas (x,y,z)
vertices = np.zeros(24, [("position", np.float32, 3)])

# preenchendo as coordenadas de cada vértice
vertices['position'] = [
    # Face 1 do Cubo (vértices do quadrado)
    (-0.2, -0.2, +0.2),
    (+0.2, -0.2, +0.2),
    (-0.2, +0.2, +0.2),
    (+0.2, +0.2, +0.2),

    # Face 2 do Cubo
    (+0.2, -0.2, +0.2),
    (+0.2, -0.2, -0.2),         
    (+0.2, +0.2, +0.2),
    (+0.2, +0.2, -0.2),
    
    # Face 3 do Cubo
    (+0.2, -0.2, -0.2),
    (-0.2, -0.2, -0.2),            
    (+0.2, +0.2, -0.2),
    (-0.2, +0.2, -0.2),

    # Face 4 do Cubo
    (-0.2, -0.2, -0.2),
    (-0.2, -0.2, +0.2),         
    (-0.2, +0.2, -0.2),
    (-0.2, +0.2, +0.2),

    # Face 5 do Cubo
    (-0.2, -0.2, -0.2),
    (+0.2, -0.2, -0.2),         
    (-0.2, -0.2, +0.2),
    (+0.2, -0.2, +0.2),
    
    # Face 6 do Cubo
    (-0.2, +0.2, +0.2),
    (+0.2, +0.2, +0.2),           
    (-0.2, +0.2, -0.2),
    (+0.2, +0.2, -0.2)
]

# Request a buffer slot from GPU
buffer = glGenBuffers(1)
# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)


# Upload data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Bind the position attribute
# --------------------------------------
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)


loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)


loc_color = glGetUniformLocation(program, "color")

glfw.show_window(window)


# translacao
x_inc = 0.0
y_inc = 0.0

# rotacao
r_inc = 0.0

# coeficiente de escala
s_inc = 1.0


def key_event(window,key,scancode,action,mods):
    global x_inc, y_inc, r_inc, s_inc
    
    if key == 263: x_inc -= 0.0001
    if key == 262: x_inc += 0.0001

    if key == 265: y_inc += 0.0001
    if key == 264: y_inc -= 0.0001
        
    if key == 65: r_inc += 0.1
    if key == 83: r_inc -= 0.1
        
    if key == 90: s_inc += 0.1
    if key == 88: s_inc -= 0.1
        
    print(key)
        
    #print(key)
    
glfw.set_key_callback(window,key_event)

import math
d = 0.0
glEnable(GL_DEPTH_TEST) ### importante para 3D

from numpy import random


def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c


loc_color = glGetUniformLocation(program, "color")
loc_transformation = glGetUniformLocation(program, "mat_transformation")

t_x = 0
t_y = 0

while not glfw.window_should_close(window):

    t_x += x_inc
    t_y += y_inc

    
    glfw.poll_events() 
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    
    ### apenas para visualizarmos o cubo rotacionando
    d -= 0.001 # modifica o angulo de rotacao em cada iteracao
    cos_d = math.cos(d)
    sin_d = math.sin(d)
    
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    mat_rotation_z = np.array([     cos_d, -sin_d, 0.0, 0.0, 
                                    sin_d,  cos_d, 0.0, 0.0, 
                                    0.0,      0.0, 1.0, 0.0, 
                                    0.0,      0.0, 0.0, 1.0], np.float32)
    
    mat_rotation_x = np.array([     1.0,   0.0,    0.0, 0.0, 
                                    0.0, cos_d, -sin_d, 0.0, 
                                    0.0, sin_d,  cos_d, 0.0, 
                                    0.0,   0.0,    0.0, 1.0], np.float32)
    
    mat_rotation_y = np.array([     cos_d,  0.0, sin_d, 0.0, 
                                    0.0,    1.0,   0.0, 0.0, 
                                    -sin_d, 0.0, cos_d, 0.0, 
                                    0.0,    0.0,   0.0, 1.0], np.float32)
    
    mat_translacao = np.array([     1.0,  0.0, 0.0,     t_x, 
                                    0.0,    1.0,   0.0, t_y, 
                                    0.0,    0.0,   1.0, 0.0, 
                                    0.0,    0.0,   0.0, 1.0], np.float32)


    # sequencia de transformações: rotação z, rotação y, rotação x, translação
    mat_transform = multiplica_matriz(mat_rotation_z,mat_rotation_y)
    mat_transform = multiplica_matriz(mat_rotation_x,mat_transform)
    mat_transform = multiplica_matriz(mat_translacao,mat_transform) #translacao ultima


    ########## Essa sequencia
    #
    #mat_transform = mat_rotation_x
    #mat_transform = multiplica_matriz(mat_translacao,mat_transform)
    #
    ############# tem o mesmo efeito que essa (ambas executam a rotação_x e depois a translação)
    #
    #mat_transform = mat_translacao
    #mat_transform = multiplica_matriz(mat_transform, mat_rotation_x)

    glUniformMatrix4fv(loc_transformation, 1, GL_TRUE, mat_transform) 
    
    
    glUniform4f(loc_color, 1, 0, 0, 1.0) ### vermelho    
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    
    glUniform4f(loc_color, 0, 0, 1, 1.0) ### azul
    glDrawArrays(GL_TRIANGLE_STRIP, 4, 4)
    
    glUniform4f(loc_color, 0, 1, 0, 1.0) ### verde
    glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
    
    glUniform4f(loc_color, 1, 1, 0, 1.0) ### amarela
    glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
    
    glUniform4f(loc_color, 0.5, 0.5, 0.5, 1.0) ### cinza
    glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
    
    glUniform4f(loc_color, 0.5, 0, 0, 1.0) ### marrom
    glDrawArrays(GL_TRIANGLE_STRIP, 20, 4)
    
    
    glfw.swap_buffers(window)

glfw.terminate()