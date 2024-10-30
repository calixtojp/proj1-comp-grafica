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
        self.plan_y = 0.8 #define o plano do chão 
        self.raio_domo = 120 #define o raio do domo do skybox
        self.raio_cabine = 3 #define o raio da cabine do alien
        self.lim_max_cacto = 3.5
        self.lim_min_cacto = 0.5


    #função que verifica se a camera pode ir um passo para frente sem
    #sair do cenário limitado pelo chão e pelo domo
    def pode_avancar(self, cameraSpeed, vetor, op):

        
        #antes de tudo fazer a operação
        if op == '+':
            self.matrix.cameraPos += cameraSpeed * vetor
        else:
            self.matrix.cameraPos -= cameraSpeed * vetor

        novo_x = self.matrix.get_camera_pos_x()
        novo_y = self.matrix.get_camera_pos_y()
        novo_z = self.matrix.get_camera_pos_z()

        #primeiro verificar o chão
        if self.matrix.get_camera_pos_y() < self.plan_y:
            if op == '+':
                self.matrix.cameraPos -= cameraSpeed * vetor
            else:
                self.matrix.cameraPos += cameraSpeed * vetor
            return False
        
        
        #agora verificar o domo
        distancia = math.sqrt(novo_x**2 + novo_y**2 + novo_z**2)
        if distancia > self.raio_domo:    
            if op == '+':
                self.matrix.cameraPos -= cameraSpeed * vetor
            else:
                self.matrix.cameraPos += cameraSpeed * vetor
            return False
        
        return True


    def key_event(self, window,key,scancode,action,mods):
        #-----------------------------------Movimentos da Camera----------------------------------#
        cameraSpeed = 0.6
        if key == 87 and (action==1 or action==2): # tecla W
            if self.pode_avancar(cameraSpeed, self.matrix.cameraFront, '+'): 
                self.matrix.cameraPos += cameraSpeed * self.matrix.cameraFront
            
        if key == 83 and (action==1 or action==2): # tecla S
            if self.pode_avancar(cameraSpeed, self.matrix.cameraFront, '-'):
                self.matrix.cameraPos -= cameraSpeed * self.matrix.cameraFront

        if key == 65 and (action==1 or action==2): # tecla A
            if self.pode_avancar(cameraSpeed, glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)), '-'):
                self.matrix.cameraPos -= glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)) * cameraSpeed
            
        if key == 68 and (action==1 or action==2): # tecla D
            if self.pode_avancar(cameraSpeed, glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)), '+'):
                self.matrix.cameraPos += glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)) * cameraSpeed

        if key == 88 and (action==1 or action==2): # tecla X
            if self.pode_avancar(cameraSpeed, self.matrix.cameraUp, '+'):
                self.matrix.cameraPos += cameraSpeed * self.matrix.cameraUp
        
        if key == 90 and (action==1 or action==2): # tecla Z
            if self.pode_avancar(cameraSpeed, self.matrix.cameraUp, '-'):
                self.matrix.cameraPos -= cameraSpeed * self.matrix.cameraUp

        #----------------------------------Modo Poligono------------------------------------------#
        if key == 80 and action==1 and self.polygonal_mode==True: #tecla P
            self.polygonal_mode=False
        else:
            if key == 80 and action==1 and self.polygonal_mode==False:
                self.polygonal_mode=True

        #------------------------------Translações e Rotações do Alien-------------------------------#
        if key == 265 and (action==1 or action==2): #Seta para Cima
            distancia = math.sqrt((self.translacao_x+0.1)**2 + (self.translacao_z)**2)
            if distancia < self.raio_cabine:    
                self.translacao_x += 0.1
        if key == 264 and (action==1 or action==2): #Seta para Baixo
            distancia = math.sqrt((self.translacao_x-0.1)**2 + (self.translacao_z)**2)
            if distancia < self.raio_cabine:    
                self.translacao_x -= 0.1
        if key == 262 and (action==1 or action==2): #Seta para Direita
            distancia = math.sqrt(self.translacao_x**2 + (self.translacao_z+0.1)**2)
            if distancia < self.raio_cabine:    
                self.translacao_z += 0.1
        if key == 263 and (action==1 or action==2): #Seta para Esquerda
            distancia = math.sqrt(self.translacao_x**2 + (self.translacao_z-0.1)**2)
            if distancia < self.raio_cabine:    
                self.translacao_z -= 0.1

        if key == 61 and (action==1 or action==2): #Mais +
            self.rotacao += 1
        if key == 45 and (action==1 or action==2): #Menos -
            self.rotacao -= 1

        #------------------------------------------Escalas dos Cactos------------------------------------------#
        if key == 77 and (action==1 or action==2) and self.escala < self.lim_max_cacto: # tecla M
            self.escala += 0.02
        if key == 78 and (action==1 or action==2) and self.escala > self.lim_min_cacto: # tecla N
            self.escala -= 0.02

            
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


        
    
