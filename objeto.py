from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import pywavefront
import glm
from shader_m import Shader
from camera import Camera, Camera_Movement
import uteis as ut
import platform, ctypes, os
from luzes import Luz
import interacoes


class Objeto:
    def __init__(self, caminho_obj, caminho_dif, caminho_spec, tam=1, trans=[0.0,0.0,0.0], angle=0, rot=[1.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0]):
        #ler .obj
        vertices = ut.ler_obj(f"objetos/{caminho_obj}")

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
        model_temp = glm.scale(model_temp, glm.vec3(scale[0], scale[1], scale[2]))
        self.model = glm.rotate(model_temp, glm.radians(angle), glm.vec3(rot[0], rot[1], rot[2]))

        #Texturas
        self.diffuse = ut.loadTexture(caminho_dif)
        self.specular = ut.loadTexture(caminho_spec)

    def desenhar(self, lightingShader, spec=1, novo=False):

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.diffuse)

        # bind specular map
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.specular)

        lightingShader.setMat4("model", self.model)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.len)