from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import pywavefront
import glm
from shader_m import Shader
from camera import Camera, Camera_Movement
import vamola
import platform, ctypes, os

class Objeto:
    def __init__(self, caminho, tam=1, trans=[0.0,0.0,0.0], angle=0, rot=[1.0, 0.0, 0.0]):
        #ler .obj
        vertices = vamola.ler_obj(caminho)

        self.len = len(vertices)

        # Configurar OBJ
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(3 * glm.sizeof(glm.float32)))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(6 * glm.sizeof(glm.float32)))
        glEnableVertexAttribArray(2)

        #Criar matriz Model
        model_temp = glm.mat4(tam)
        model_temp = glm.translate(model_temp, glm.vec3( trans[0],  trans[1],  trans[2]))
        self.model = glm.rotate(model_temp, glm.radians(angle), glm.vec3(rot[0], rot[1], rot[2]))