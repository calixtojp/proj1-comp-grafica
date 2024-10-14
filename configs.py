import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
import glm

class Configuracoes:
    def __init__(self, largura, altura):  
        self.largura = largura
        self.altura = altura

    def janela(self):
        #Essa função garante configurações iniciais da janela

        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(self.largura, self.altura, "Projeto 2", None, None)
        glfw.make_context_current(window)
        glfw.show_window(window)

        #Isso garante que o OpenGL renderize objetos 3D corretamente, levando em consideração 
        #a profundidade dos vértices e ocultando superfícies que deveriam estar atrás de outras.
        glEnable(GL_DEPTH_TEST) ### importante para 3D

        return window

    def programa(self):
        #Essa função garante configurações iniciais do programa

        vertex_code = """
                attribute vec3 position;
                attribute vec2 texture_coord;
                varying vec2 out_texture;
                        
                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;        
                
                void main(){
                    gl_Position = projection * view * model * vec4(position,1.0);
                    out_texture = vec2(texture_coord);
                }
                """
        
        fragment_code = """
                uniform vec4 color;
                varying vec2 out_texture;
                uniform sampler2D samplerTexture;
                
                void main(){
                    vec4 texture = texture2D(samplerTexture, out_texture);
                    gl_FragColor = texture;
                }
                """
        
        # Pedindo programa e slots de shader para a GPU
        program  = glCreateProgram()
        vertex   = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        # Definindo fonte do shader
        glShaderSource(vertex, vertex_code)
        glShaderSource(fragment, fragment_code)

        # Compilando shaders
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

        # Atribuindo objetos do shader para o programa
        glAttachShader(program, vertex)
        glAttachShader(program, fragment)

        # Criando programa
        glLinkProgram(program)
        if not glGetProgramiv(program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(program))
            raise RuntimeError('Linking error')
            
        # Fazendo esse programa ser o padrão
        glUseProgram(program)
        return program

    def passar_para_gpu(self, program, item, modo):
        #função que passa os objetos ou as texturas para a GPU a partir de um programa a depender do modo escolhido

        #configurações padrão para passar os vértices
        shader_var = "position"
        num = 3

        #caso queiramos passar a textura, alteramos as config
        if(modo=="textura"):
            shader_var = "texture_coord"
            num = 2

        # Pedindo um buffer para a GPU
        buffer = glGenBuffers(1)

        # Tornando esse buffer o padrão
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        # Fazendo upload dos dados 
        glBufferData(GL_ARRAY_BUFFER, item.nbytes, item, GL_STATIC_DRAW)

        # Calcula o espaçamento entre os dados de vértices no buffer
        stride = item.strides[0]
        offset = ctypes.c_void_p(0)

        # Conecta o atributo de posição do buffer com o shader
        loc = glGetAttribLocation(program, shader_var)
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, num, GL_FLOAT, False, stride, offset)
