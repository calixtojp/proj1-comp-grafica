
from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import glm
import platform, ctypes, os
import interacoes as it

def config_inicial():
    glfwInit()
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    if (platform.system() == "Darwin"): # APPLE
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfwCreateWindow(it.SCR_WIDTH, it.SCR_HEIGHT, "LearnOpenGL", None, None)
    if (window == None):

        print("Failed to create GLFW window")
        glfwTerminate()

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, it.framebuffer_size_callback)
    glfwSetCursorPosCallback(window, it.mouse_callback)
    glfwSetScrollCallback(window, it.scroll_callback)

    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)

    return window


# abre o arquivo obj para leitura
def ler_obj(caminho):
    # Load the OBJ file
    vertices = []
    normals = [] # apareceu no código de iluminação
    texture_coords = []
    faces = []

    material = None

    for line in open(caminho, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue


        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])

        ### recuperando normal
        if values[0] == 'vn':
            normals.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normals = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, face_normals, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces
    model['normals'] = normals 

    # Convert to glm array (similar to your cube's vertices)
    # Flattened vertices array for OpenGL
    final_vertices = []

    # Parse each face
    for face, face_texture, face_normals, material in model['faces']:
        for i in range(len(face)):  # Each vertex in the face
            # Vertex position
            vertex_index = face[i] - 1  # .obj indices are 1-based
            position = list(map(float, model['vertices'][vertex_index]))

            # Normal (if exists)
            if face_normals[i] > 0:
                normal_index = face_normals[i] - 1
                normal = list(map(float, model['normals'][normal_index]))
            else:
                normal = [0.0, 0.0, 0.0]  # Default normal

            # Texture coordinate (if exists)
            if face_texture[i] > 0:
                tex_index = face_texture[i] - 1
                tex_coord = list(map(float, model['texture'][tex_index]))
            else:
                tex_coord = [0.0, 0.0]  # Default texture coordinate

            # Combine into one array (position + normal + texture coordinate)
            final_vertices.extend(position + normal + tex_coord)

    return glm.array(glm.float32, *final_vertices)


# utility function for loading a 2D texture from file
# ---------------------------------------------------

# the relative path where the textures are located
IMAGE_RESOURCE_PATH = "./texturas/"

# function that loads and automatically flips an image vertically
LOAD_IMAGE = lambda name: Image.open(os.path.join(IMAGE_RESOURCE_PATH, name)).transpose(Image.FLIP_TOP_BOTTOM)

def loadTexture(path: str) -> int:

    textureID = glGenTextures(1)
    

    img = LOAD_IMAGE(path)

    nrComponents = len(img.getbands())

    format = GL_RED if nrComponents == 1 else \
                GL_RGB if nrComponents == 3 else \
                GL_RGBA 

    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexImage2D(GL_TEXTURE_2D, 0, format, img.width, img.height, 0, format, GL_UNSIGNED_BYTE, img.tobytes())
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img.close()

    return textureID