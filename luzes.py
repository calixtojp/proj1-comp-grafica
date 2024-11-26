from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import glm
import platform, ctypes, os

from shader_m import Shader
import interacoes as it

class Luz:

    def __init__(self, ambient_=1, diffuse_=1, specular_=1):
        self.lightingShader = Shader("shaders/6.multiple_lights.vs", "shaders/6.multiple_lights.fs")
        self.lightCubeShader = Shader("shaders/6.light_cube.vs", "shaders/6.light_cube.fs")

        # shader configuration
        self.lightingShader.use()
        self.lightingShader.setInt("material.diffuse", 0)
        self.lightingShader.setInt("material.specular", 1)

        # world transformation
        model = glm.mat4(1.0)
        self.lightingShader.setMat4("model", model)

        self.pos = [
                        glm.vec3(it.nave_x,  it.nave_y,  it.nave_z),
                        glm.vec3(it.nave_x, it.nave_y, it.nave_z),
                        glm.vec3(it.nave_x+2.05, it.nave_y, it.nave_z+0.5)
                    ]

        self.ambient = ambient_
        self.diffuse = diffuse_
        self.specular = specular_

    def preProcObj(self):
        # be sure to activate shader when setting uniforms/drawing objects
        self.lightingShader.use()
        self.lightingShader.setVec3("viewPos", it.camera.Position)
        self.lightingShader.setFloat("material.shininess", 32.0)
    
    def preProcLampada(self, projection, view):
        self.lightCubeShader.use()
        self.lightCubeShader.setMat4("projection", projection)
        self.lightCubeShader.setMat4("view", view)
    
    def aplicar(self):

        #   Here we set all the uniforms for the 5/6 types of lights we have. We have to set them manually and index 
        #   the proper PointLight struct in the array to set each uniform variable. This can be done more code-friendly
        #   by defining light types as classes and set their values in there, or by using a more efficient uniform approach
        #   by using 'Uniform buffer objects', but that is something we'll discuss in the 'Advanced GLSL' tutorial.

        # directional light
        self.lightingShader.setVec3("dirLight.direction", -0.2, -1.0, -0.3)
        self.lightingShader.setVec3("dirLight.ambient", it.toggle_dir*self.ambient*it.amb*0.05, it.toggle_dir*self.ambient*it.amb*0.05, it.toggle_dir*self.ambient*it.amb*0.05)
        self.lightingShader.setVec3("dirLight.diffuse", it.toggle_dir*self.diffuse*it.dif*0.4, it.toggle_dir*self.diffuse*it.dif*0.4, it.toggle_dir*self.diffuse*it.dif*0.4)
        self.lightingShader.setVec3("dirLight.specular", it.toggle_dir*self.specular*it.spec*0.5, it.toggle_dir*self.specular*it.spec*0.5, it.toggle_dir*self.specular*it.spec*0.5)
        # point light 1 (luz da parte de baixo da nave, externa) => EXTERNA
        self.lightingShader.setVec3("pointLights[0].position", self.pos[0])
        self.lightingShader.setVec3("pointLights[0].ambient", it.toggle_ex*it.toggle_pl1*self.ambient*it.amb*0.05, it.toggle_ex*it.toggle_pl1*self.ambient*it.amb*0.05, it.toggle_ex*it.toggle_pl1*self.ambient*it.amb*0.05)
        self.lightingShader.setVec3("pointLights[0].diffuse", it.toggle_ex*it.toggle_pl1*self.diffuse*it.dif*0.8, it.toggle_ex*it.toggle_pl1*self.diffuse*it.dif*0.8, it.toggle_ex*it.toggle_pl1*self.diffuse*it.dif*0.8)
        self.lightingShader.setVec3("pointLights[0].specular", it.toggle_ex*it.toggle_pl1*self.specular*it.spec*1.0, it.toggle_ex*it.toggle_pl1*self.specular*it.spec*1.0, it.toggle_ex*it.toggle_pl1*self.specular*it.spec*1.0)
        self.lightingShader.setFloat("pointLights[0].constant", 1.0)
        self.lightingShader.setFloat("pointLights[0].linear", 0.09)
        self.lightingShader.setFloat("pointLights[0].quadratic", 0.032)
        # point light 2 (luz da parte de baixo da nave, interna) => INTERNA
        self.lightingShader.setVec3("pointLights[1].position", self.pos[1])
        self.lightingShader.setVec3("pointLights[1].ambient", it.toggle_in*it.toggle_pl2*self.ambient*it.amb*0.05, it.toggle_in*it.toggle_pl2*self.ambient*it.amb*0.05, it.toggle_in*it.toggle_pl2*self.ambient*it.amb*0.05)
        self.lightingShader.setVec3("pointLights[1].diffuse", it.toggle_in*it.toggle_pl2*self.diffuse*it.dif*0.8, it.toggle_in*it.toggle_pl2*self.diffuse*it.dif*0.8, it.toggle_in*it.toggle_pl2*self.diffuse*it.dif*0.8)
        self.lightingShader.setVec3("pointLights[1].specular", it.toggle_in*it.toggle_pl2*self.specular*it.spec*1.0, it.toggle_in*it.toggle_pl2*self.specular*it.spec*1.0, it.toggle_in*it.toggle_pl2*self.specular*it.spec*1.0)
        self.lightingShader.setFloat("pointLights[1].constant", 1.0)
        self.lightingShader.setFloat("pointLights[1].linear", 0.09)
        self.lightingShader.setFloat("pointLights[1].quadratic", 0.032)
        # point light 3 (luz da tocha do minion) => => INTERNA
        self.lightingShader.setVec3("pointLights[2].position", self.pos[2])
        self.lightingShader.setVec3("pointLights[2].ambient", it.toggle_in*it.toggle_pl3*self.ambient*it.amb*0.2, it.toggle_in*it.toggle_pl3*self.ambient*it.amb*0.0, it.toggle_in*it.toggle_pl3*self.ambient*it.amb*0.00)
        self.lightingShader.setVec3("pointLights[2].diffuse", it.toggle_in*it.toggle_pl3*self.diffuse*it.dif*1.0, it.toggle_in*it.toggle_pl3*self.diffuse*it.dif*0.2, it.toggle_in*it.toggle_pl3*self.diffuse*it.dif*0.0)
        self.lightingShader.setVec3("pointLights[2].specular", it.toggle_in*it.toggle_pl3*self.specular*it.spec*0.8, it.toggle_in*it.toggle_pl3*self.specular*it.spec*0.4, it.toggle_in*it.toggle_pl3*self.specular*it.spec*0.2)
        self.lightingShader.setFloat("pointLights[2].constant", 1.0)
        self.lightingShader.setFloat("pointLights[2].linear", 0.09)
        self.lightingShader.setFloat("pointLights[2].quadratic", 0.032)
        # spotLight (luz do cone de abdução da nave) => EXTERNA
        self.lightingShader.setVec3("spotLight.position", glm.vec3(it.nave_x,30,it.nave_z))
        self.lightingShader.setVec3("spotLight.direction", glm.vec3(0,-1,0))
        self.lightingShader.setVec3("spotLight.ambient", it.toggle_ex*it.toggle_sl*self.ambient*it.amb*0.0, it.toggle_ex*it.toggle_sl*self.ambient*it.amb*0.2, it.toggle_ex*it.toggle_sl*self.ambient*it.amb*0.0)
        self.lightingShader.setVec3("spotLight.diffuse", it.toggle_ex*it.toggle_sl*self.diffuse*it.dif*1.05, it.toggle_ex*it.toggle_sl*self.diffuse*it.dif*1.46, it.toggle_ex*it.toggle_sl*self.diffuse*it.dif*1.07)
        self.lightingShader.setVec3("spotLight.specular", it.toggle_ex*it.toggle_sl*self.specular*it.spec*0.1, it.toggle_ex*it.toggle_sl*self.specular*it.spec*0.4, it.toggle_ex*it.toggle_sl*self.specular*it.spec*0.1)
        self.lightingShader.setFloat("spotLight.constant", 1.0)
        self.lightingShader.setFloat("spotLight.linear", 0.01)
        self.lightingShader.setFloat("spotLight.quadratic", 0.002)
        self.lightingShader.setFloat("spotLight.cutOff", glm.cos(glm.radians(40)))
        self.lightingShader.setFloat("spotLight.outerCutOff", glm.cos(glm.radians(45)))     

    def configurar_iluminacao(self, ambient_=1, diffuse_=1, specular_=1):
        self.ambient = ambient_
        self.diffuse = diffuse_
        self.specular = specular_

        self.preProcObj()
        self.aplicar()

        # view/projection transformations
        projection = glm.perspective(glm.radians(it.camera.Zoom), it.SCR_WIDTH / it.SCR_HEIGHT, 0.1, 1000.0)
        view = it.camera.GetViewMatrix()
        self.lightingShader.setMat4("projection", projection)
        self.lightingShader.setMat4("view", view)
