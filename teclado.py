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

    def key_event(self, window,key,scancode,action,mods):
        print(key)
        if key == 66:
            inc_view_up += 0.1
            #cameraUp    = glm.vec3(0.0+inc_view_up,  1.0+inc_view_up,  0.0+inc_view_up);
        if key == 78: inc_near += 0.1
        if key == 77: inc_far -= 5
            
        cameraSpeed = 0.2
        if key == 87 and (action==1 or action==2): # tecla W
            self.matrix.cameraPos += cameraSpeed * self.matrix.cameraFront
        
        if key == 83 and (action==1 or action==2): # tecla S
            self.matrix.cameraPos -= cameraSpeed * self.matrix.cameraFront
        
        if key == 65 and (action==1 or action==2): # tecla A
            self.matrix.cameraPos -= glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)) * cameraSpeed
            
        if key == 68 and (action==1 or action==2): # tecla D
            self.matrix.cameraPos += glm.normalize(glm.cross(self.matrix.cameraFront, self.matrix.cameraUp)) * cameraSpeed
            
        if key == 80 and action==1 and self.polygonal_mode==True:
            self.polygonal_mode=False
        else:
            if key == 80 and action==1 and self.polygonal_mode==False:
                self.polygonal_mode=True
            
    def mouse_event(self, window, xpos, ypos):
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        print(self.lastX, "lastX")
        print(self.lastY, "lastY")

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


        
    
