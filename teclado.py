import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math

class Teclado:
    def __init__(self, matrix):
        self.polygonal_mode = False
        self.matrix = matrix

        self.firstMouse = True
        self.yaw = -90.0 
        self.pitch = 0.0
        self.lastX =  self.matrix.c.largura/2
        self.lastY =  self.matrix.c.altura/2

        #variáveis de transformações nos objetos
        self.escala = 1
        self.rotacao = 1
        self.translacao_x = 0
        self.translacao_y = 0
        self.translacao_z = 0

        #variáveis que definem os limites da movimentação da câmera dentro do cenário
        self.plan_y = 0#define o plano do chão 
        self.raio_domo = 100#define o raio do domo do skybox
        self.lim_max_cacto = 3.5
        self.lim_min_cacto = 0.5


    def key_event(self, window,key,scancode,action,mods):
        if key == 66:
            inc_view_up += 0.1
                
        #Moviimentos da Camera
        cameraSpeed = 0.6
        if key == 87 and (action==1 or action==2): # tecla W
            self.matrix.cameraPos += cameraSpeed * self.matrix.cameraFront
        
        if key == 83 and (action==1 or action==2): # tecla S
            self.matrix.cameraPos -= cameraSpeed * self.matrix.cameraFront

        if key == 65 and (action==1 or action==2): # tecla A
            self.matrix.cameraPos -= glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)) * cameraSpeed
            
        if key == 68 and (action==1 or action==2): # tecla D
            self.matrix.cameraPos += glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)) * cameraSpeed

        if key == 88 and (action==1 or action==2): # tecla X
            self.matrix.cameraPos += cameraSpeed * self.matrix.cameraUp
        
        if key == 90 and (action==1 or action==2): # tecla Z
            self.matrix.cameraPos -= cameraSpeed * self.matrix.cameraUp


        if key == 80 and action==1 and self.polygonal_mode==True: #tecla P
            self.polygonal_mode=False
        else:
            if key == 80 and action==1 and self.polygonal_mode==False:
                self.polygonal_mode=True

        #=========== transformações nos objetos ===========
        #transalção em X e Z:
        #No eixo X: tecla R aumenta e F diminui
        if key == 82 and (action==1 or action==2):
            self.translacao_x += 0.1
        if key == 70 and (action==1 or action==2):
            self.translacao_x -= 0.1
        #No eixo Z: tecla Y aumenta e H diminui
        if key == 89 and (action==1 or action==2):
            self.translacao_z += 0.1
        if key == 72 and (action==1 or action==2):
            self.translacao_z -= 0.1

        #escala (tecla M para aumentar e N para diminuir)
        if key == 77 and (action==1 or action==2) and self.escala < self.lim_max_cacto:
            self.escala += 0.02
        if key == 78 and (action==1 or action==2) and self.escala > self.lim_min_cacto:
            self.escala -= 0.02

        #rotação (tecla Z para aumentar e X para diminuir)
        if key == 90 and (action==1 or action==2):
            self.rotacao += 0.4
        if key == 88 and (action==1 or action==2):
            self.rotacao -= 0.4

            
    def mouse_event(self, window, xpos, ypos):
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos
        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.3
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        
        if self.pitch >= 90.0: self.pitch = 90.0
        if self.pitch <= -90.0: self.pitch = -90.0

        front = glm.vec3()
        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        self.matrix.cameraFront = glm.normalize(front)


        
    
