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
                attribute vec3 normals;
                
            
                varying vec2 out_texture;
                varying vec3 out_fragPos; //posicao do fragmento (i.e., posicao na superficie onde a iluminacao sera calculada)
                varying vec3 out_normal;
                        
                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;        
                
                void main(){
                    gl_Position = projection * view * model * vec4(position,1.0);
                    out_texture = vec2(texture_coord);
                    out_fragPos = vec3(  model * vec4(position, 1.0));
                    out_normal = vec3( model *vec4(normals, 1.0));            
                }
                """
        
        fragment_code = """
    
            // parametro com a cor da(s) fonte(s) de iluminacao
            uniform vec3 lightPos; // define coordenadas de posicao da luz
            vec3 lightColor = vec3(1.0, 1.0, 1.0);
            
            // parametros da iluminacao ambiente e difusa
            uniform float ka; // coeficiente de reflexao ambiente
            uniform float kd; // coeficiente de reflexao difusa
            
            // parametros da iluminacao especular
            uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
            uniform float ks; // coeficiente de reflexao especular
            uniform float ns; // expoente de reflexao especular
            
    
    
            // parametros recebidos do vertex shader
            varying vec2 out_texture; // recebido do vertex shader
            varying vec3 out_normal; // recebido do vertex shader
            varying vec3 out_fragPos; // recebido do vertex shader
            uniform sampler2D samplerTexture;
            
            
            
            void main(){
            
                // calculando reflexao ambiente
                vec3 ambient = ka * lightColor;             
            
                // calculando reflexao difusa
                vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
                vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
                float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
                vec3 diffuse = kd * diff * lightColor; // iluminacao difusa
                
                // calculando reflexao especular
                vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera
                vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao
                float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
                
                vec3 specular = ks * spec * lightColor;             
                
                // aplicando o modelo de iluminacao
                vec4 texture = texture2D(samplerTexture, out_texture);
                vec4 result = vec4((ambient + diffuse + specular),1.0) * texture; // aplica iluminacao
                gl_FragColor = result;
    
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
        if(modo =="textura"):
            shader_var = "texture_coord"
            num = 2
        elif(modo == "iluminacao"):
            shader_var = "normals"
            num = 3

        # print(f'passar GPU| modo>{modo} | shader_var>{shader_var} | num>{num}')

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
