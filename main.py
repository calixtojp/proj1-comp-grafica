import glfw
from OpenGL.GL import *
import numpy as np
from configs import Configuracoes
from matrizes import Matrizes
from teclado import Teclado
from models import Models
from objeto import Objeto
import math

# só pra testa

def main():
    # Configurações iniciais
    c = Configuracoes(1600, 1200)
    matrix = Matrizes(c)
    m = Models()
    t = Teclado(matrix)

    # Parâmetros para objetos
    qtd_cactos = 5
    espalhamento_cactos = 80.0
    qtd_pedras = 7
    espalhamento_pedras = 60.0
    qtd_vacas = 3
    espalhamento_vacas = 40.0
    qtd_minions = 6
    raio_minions = 12.0

    # Inicializando a janela e o programa
    window = c.janela()
    program = c.programa()

    # Criando listas de objetos e outros objetos fixos
    objetos = {
        "cactos": [Objeto(matrix, m, 'cacto/cacto.obj', 'cacto/cacto.jpg', 0) for _ in range(qtd_cactos)],
        "pedras": [Objeto(matrix, m, 'pedra/pedra.obj', 'pedra/pedra.jpg', 1) for _ in range(qtd_pedras)],
        "vacas": [Objeto(matrix, m, 'vaca/vaca.obj', 'vaca/vaca.jpeg', 2) for _ in range(qtd_vacas)],
        "minions": [Objeto(matrix, m, 'minion/minion.obj', 'minion/minion.png', 3) for _ in range(qtd_minions)],
        "ceu": Objeto(matrix, m, 'ceu/esfera.obj', 'ceu/nightSky.jpg', 4),
        "chao": Objeto(matrix, m, 'chao/chao.obj', 'chao/chao.jpg', 5),
        "nave": Objeto(matrix, m, 'nave/nave.obj', 'nave/nave.png', 6),
        "alien": Objeto(matrix, m, 'alien/alien.obj', 'alien/alien.jpg', 7),
        "cj": Objeto(matrix, m, 'cj/cj.obj', 'cj/cj.jpg', 8)
    }

    # Concatenando vértices e texturas
    vertices = np.concatenate(
        [obj.vertices_list for obj in objetos["cactos"]] + 
        [obj.vertices_list for obj in objetos["pedras"]] + 
        [obj.vertices_list for obj in objetos["vacas"]] +
        [obj.vertices_list for obj in objetos["minions"]] +
        [objetos["ceu"].vertices_list,
        objetos["chao"].vertices_list,
        objetos["nave"].vertices_list,
        objetos["alien"].vertices_list,
        objetos["cj"].vertices_list]
    )

    total_vertices = len(vertices)
    merged_vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
    merged_vertices['position'] = vertices

    textures = np.concatenate(
        [obj.textures_coord_list for obj in objetos["cactos"]] + 
        [obj.textures_coord_list for obj in objetos["pedras"]] + 
        [obj.textures_coord_list for obj in objetos["vacas"]] +
        [obj.textures_coord_list for obj in objetos["minions"]] +
        [objetos["ceu"].textures_coord_list,
        objetos["chao"].textures_coord_list,
        objetos["nave"].textures_coord_list,
        objetos["alien"].textures_coord_list,
        objetos["cj"].textures_coord_list]
    )
    total_textures = len(textures)
    merged_texture = np.zeros(total_textures, [("position", np.float32, 2)])
    merged_texture['position'] = textures

    # Passando vértices e texturas para a GPU
    c.passar_para_gpu(program, merged_vertices, "vertices")
    c.passar_para_gpu(program, merged_texture, "textura")

    # Configurando o teclado
    glfw.set_key_callback(window, t.key_event)
    glfw.set_cursor_pos_callback(window, t.mouse_event)

    # Configurando posições iniciais e espalhamento para cada tipo de objeto
    pos_ini_cacto_x, pos_ini_cacto_z = 15.0, -5.0
    pos_ini_pedra_x, pos_ini_pedra_z = 5, -4
    pos_ini_vaca_x, pos_ini_vaca_z = -4, 5

    cactos_posicoes = [(pos_ini_cacto_x, pos_ini_cacto_z)]
    pedras_posicoes = [(pos_ini_pedra_x, pos_ini_pedra_z)]
    vacas_posicoes = [(pos_ini_vaca_x, pos_ini_vaca_z)]

    # Gerando posições aleatórias para cada instância dos objetos
    for _ in range(1, qtd_cactos):
        pos_x = np.random.uniform(pos_ini_cacto_x - espalhamento_cactos, pos_ini_cacto_x + espalhamento_cactos)
        pos_z = np.random.uniform(pos_ini_cacto_z - espalhamento_cactos, pos_ini_cacto_z + espalhamento_cactos)
        cactos_posicoes.append((pos_x, pos_z))

    for _ in range(1, qtd_pedras):
        pos_x = np.random.uniform(pos_ini_pedra_x - espalhamento_pedras, pos_ini_pedra_x + espalhamento_pedras)
        pos_z = np.random.uniform(pos_ini_pedra_z - espalhamento_pedras, pos_ini_pedra_z + espalhamento_pedras)
        pedras_posicoes.append((pos_x, pos_z))

    for _ in range(1, qtd_vacas):
        pos_x = np.random.uniform(pos_ini_vaca_x - espalhamento_vacas, pos_ini_vaca_x + espalhamento_vacas)
        pos_z = np.random.uniform(pos_ini_vaca_z - espalhamento_vacas, pos_ini_vaca_z + espalhamento_vacas)
        vacas_posicoes.append((pos_x, pos_z))

    # Loop principal que exibe a janela
    rotacao_cj = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.44, 0.6, 0.7, 1.0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if t.polygonal_mode else GL_FILL)

        # Desenhando cactos
        pos = 0
        for i, cacto in enumerate(objetos["cactos"]):
            pos_x, pos_z = cactos_posicoes[i]
            cacto.desenha(program, pos, -90, 1, 0, 0, pos_x, 0, pos_z, 0.1, 0.1, 0.03*t.escala)
            pos += len(cacto.vertices_list)

        # Desenhando pedras
        for i, pedra in enumerate(objetos["pedras"]):
            pos_x, pos_z = pedras_posicoes[i]
            pedra.desenha(program, pos, 0, 0, 0, 1, pos_x, -0.5, pos_z, 0.01, 0.01, 0.01)
            pos += len(pedra.vertices_list)

        # Desenhando vacas
        for i, vaca in enumerate(objetos["vacas"]):
            pos_x, pos_z = vacas_posicoes[i]
            vaca.desenha(program, pos, 30, 0, 0, 1, pos_x, 1, pos_z, 1, 1, 1)
            pos += len(vaca.vertices_list)

        # Desenhando minions
        angulo_inicial = 0
        incremento_angulo = 360 / qtd_minions
        for i, minion in enumerate(objetos["minions"]):
            angulo_rad = math.radians(angulo_inicial + i * incremento_angulo)
            pos_x = raio_minions * math.cos(angulo_rad)
            pos_z = raio_minions * math.sin(angulo_rad)
            minion.desenha(program, pos, -incremento_angulo*(i)-90, 0, 1, 0, pos_x, 43, pos_z, 0.2, 0.2, 0.2)
            pos += len(minion.vertices_list)


        # Desenhando ceu 
        objetos["ceu"].desenha(program, pos, 0, 0, 0, 1, -1200, -400, 200, 200, 200, 200)
        pos += len(objetos["ceu"].vertices_list)

        # Desenhando chao
        objetos["chao"].desenha(program, pos, 0, 0, 0, 1, 0, -5, 0, 2, 0.5, 2)
        pos += len(objetos["chao"].vertices_list)

        # Desenhando nave
        objetos["nave"].desenha(program, pos, 0, 0, 1, 0, 0, 32, 0, 0.7, 0.7, 0.7)
        pos += len(objetos["nave"].vertices_list)

        #Desenhando alien
        objetos["alien"].desenha(program, pos, 135+t.rotacao, 0, 1, 0, t.translacao_x, 49.5, t.translacao_z, 0.03, 0.03, 0.03)
        pos += len(objetos["alien"].vertices_list)

        #Desenhando cj
        objetos["cj"].desenha(program, pos, rotacao_cj, 1, 1, 1, 0, 44, 0, 2, 2, 2)
        pos += len(objetos["cj"].vertices_list)
        rotacao_cj = (rotacao_cj + 1) % 360

        # Configuração das matrizes view e projection
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, matrix.view())

        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, matrix.projection())

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
