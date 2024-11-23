from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import glm
import platform, ctypes, os

from shader_m import Shader
import interacoes as it

class Luz:
    def __init__(self):
        self.lightingShader = Shader("shaders/6.multiple_lights.vs", "shaders/6.multiple_lights.fs")
        self.lightCubeShader = Shader("shaders/6.light_cube.vs", "shaders/6.light_cube.fs")
    

    def configurar(self):
        # shader configuration
        # --------------------
        self.lightingShader.use()
        self.lightingShader.setInt("material.diffuse", 0)
        self.lightingShader.setInt("material.specular", 1)
        
        # world transformation
        model = glm.mat4(1.0)
        self.lightingShader.setMat4("model", model)


    def aplicar(self):
        # be sure to activate shader when setting uniforms/drawing objects
        self.lightingShader.use()
        self.lightingShader.setVec3("viewPos", it.camera.Position)
        self.lightingShader.setFloat("material.shininess", 32.0)

        #   Here we set all the uniforms for the 5/6 types of lights we have. We have to set them manually and index 
        #   the proper PointLight struct in the array to set each uniform variable. This can be done more code-friendly
        #   by defining light types as classes and set their values in there, or by using a more efficient uniform approach
        #   by using 'Uniform buffer objects', but that is something we'll discuss in the 'Advanced GLSL' tutorial.
            
        s = 1
        d = 1
        a = 1

        self.pos = [glm.vec3( 10.7,  0.2,  2.0), glm.vec3( -10.3, -3.3, -4.0)]

        # directional light
        self.lightingShader.setVec3("dirLight.direction", -0.2, -1.0, -0.3)
        self.lightingShader.setVec3("dirLight.ambient", a*0.05, a*0.05, a*0.05)
        self.lightingShader.setVec3("dirLight.diffuse", d*0.4, d*0.4, d*0.4)
        self.lightingShader.setVec3("dirLight.specular", s*0.5, s*0.5, s*0.5)
        # point light 1
        self.lightingShader.setVec3("pointLights[0].position", self.pos[0])
        self.lightingShader.setVec3("pointLights[0].ambient", a*0.05, a*0.05, a*0.05)
        self.lightingShader.setVec3("pointLights[0].diffuse", d*0.8, d*0.8, d*0.8)
        self.lightingShader.setVec3("pointLights[0].specular", s*1.0, s*1.0, s*1.0)
        self.lightingShader.setFloat("pointLights[0].constant", 1.0)
        self.lightingShader.setFloat("pointLights[0].linear", 0.09)
        self.lightingShader.setFloat("pointLights[0].quadratic", 0.032)
        # point light 2
        self.lightingShader.setVec3("pointLights[1].position", self.pos[1])
        self.lightingShader.setVec3("pointLights[1].ambient", a*0.05, a*0.05, a*0.05)
        self.lightingShader.setVec3("pointLights[1].diffuse", d*0.8, d*0.8, d*0.8)
        self.lightingShader.setVec3("pointLights[1].specular", s*1.0, s*1.0, s*1.0)
        self.lightingShader.setFloat("pointLights[1].constant", 1.0)
        self.lightingShader.setFloat("pointLights[1].linear", 0.09)
        self.lightingShader.setFloat("pointLights[1].quadratic", 0.032)
        # spotLight
        self.lightingShader.setVec3("spotLight.position", it.camera.Position)
        self.lightingShader.setVec3("spotLight.direction", it.camera.Front)
        self.lightingShader.setVec3("spotLight.ambient", a*0.0, a*0.0, a*0.0)
        self.lightingShader.setVec3("spotLight.diffuse", d*1.0, d*1.0, d*1.0)
        self.lightingShader.setVec3("spotLight.specular", s*1.0, s*1.0, s*1.0)
        self.lightingShader.setFloat("spotLight.constant", 1.0)
        self.lightingShader.setFloat("spotLight.linear", 0.09)
        self.lightingShader.setFloat("spotLight.quadratic", 0.032)
        self.lightingShader.setFloat("spotLight.cutOff", glm.cos(glm.radians(12.5)))
        self.lightingShader.setFloat("spotLight.outerCutOff", glm.cos(glm.radians(15.0)))     