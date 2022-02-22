from argparse import Action
from pickle import POP_MARK
from OpenGL.GL import *
from glew_wish import *
import glfw
import math

#unidades por segundo
velocidad = 0.8
posicion_mosca = [0,-1,0]
angulo_mosca = 0
posicion_triangulo = [0.0,-0.95,0.0]
posiciones_cuadrados = [
     [0.3,-0.85, 0.0],
     [0.8, -0.75, 0.0],
     [-0.4, -0.65, 0.0],
     [0.2, -0.55, 0.0],
     [0.7, -0.45, 0.0],
     [-0.1, -0.55, 0.0],
     [-0.3, -0.25, 0.0],
     [-0.6, -0.15, 0.0],
     [-0.2, -0.05, 0.0],
     [0.5, 0.05, 0.0],
     [0.3, 0.15, 0.0],
     [0.7, 0.25, 0.0],
     [0.9, 0.75, 0.0],
     [0.2, 0.45, 0.0],
     [-0.4, 0.55, 0.0],
     [-0.2, 0.65, 0.0],
     [0.5, 0.75, 0.0],
     [0.2, 0.85, 0.0],
     #mas cuadros
     [0.5,-0.85, 0.0],
     [0.5, -0.75, 0.0],
     [-0.9, -0.65, 0.0],
     [0.8, -0.55, 0.0],
     [0.9, -0.45, 0.0],
     [-0.8, -0.85, 0.0],
     [-0.7, -0.25, 0.0],
     [-0.2, -0.15, 0.0],
     [-0.5, -0.05, 0.0],
     [0.9, 0.05, 0.0],
     [0.7, 0.15, 0.0],
     [0.2, 0.25, 0.0],
     [0.7, 0.65, 0.0],
     [0.5, 0.45, 0.0]
     
 ]


velocidades_cuadrados=[0.5, 0.6, 0.5, 0.7, 0.5, 0.8, 0.5, 0.9, 0.5, 0.6, 0.5, 0.7, 0.5, 0.8, 0.5, 0.9, 0.5, 0.6, 0.5, 0.8, 0.5, 0.9, 0.5, 0.6, 0.5, 0.7, 0.5, 0.8, 0.9, 0.5]
direcciones_cuadrados=[2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

window = None
velocidad_triangulo = 0.1
velocidad_rotacion_triangulo = 90.0
fase = 90.0

tiempo_anterior = 0.0

#0 arriba , 1 abajo, 2 izquierda, 3 derecha
direccion_triangulo = 0
angulo_triangulo = 0
direccion_derecha = 3
direccion_izquierda = 2

def actualizar():

    global tiempo_anterior
    global window
    global posicion_triangulo
    global direccion_triangulo
    global angulo_triangulo
    global velocidad_triangulo

    tiempo_actual = glfw.get_time()
    tiempo_delta = tiempo_actual - tiempo_anterior
    
    actualizar_mosca(tiempo_delta)
    for i in range(30):
        cantidad_movimiento = velocidades_cuadrados[i] * tiempo_delta
        if direcciones_cuadrados[i] == 2:
            posiciones_cuadrados[i][0] = posiciones_cuadrados[i][0] - cantidad_movimiento
            if posiciones_cuadrados[i][0] <= -1:
                posiciones_cuadrados[i][0] = 1
        if direcciones_cuadrados[i] == 3:
            posiciones_cuadrados[i][0] = posiciones_cuadrados[i][0] + cantidad_movimiento
            if posiciones_cuadrados[i][0] >= 1:
                posiciones_cuadrados[i][0] = -1
    tiempo_anterior = tiempo_actual

def actualizar_mosca(tiempo_delta):
    global posicion_mosca
    global angulo_mosca
    fase= 90
    cantidad_movimiento = 0.6 * tiempo_delta
    posicion_mosca[0] = posicion_mosca[0] + (math.cos((angulo_mosca + fase) * math.pi/ 180)  * cantidad_movimiento )
    posicion_mosca[1] = posicion_mosca[1] + (math.sin((angulo_mosca + fase) * math.pi/ 180)  * cantidad_movimiento )

    angulo_mosca = angulo_mosca + 0.2

def key_callback(window, key, scancode, action, mods):
    global posicion_triangulo
    global velocidad_triangulo

    #Que la tecla escape cierre ventana al ser presionada
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window,1)

    #MOVER LA RANA
     #IZQUIERDA
    if key == glfw.KEY_LEFT and (action == glfw.PRESS):
        posicion_triangulo[0] =  posicion_triangulo[0] - velocidad_triangulo
    #DERECHA
    if key == glfw.KEY_RIGHT and (action == glfw.PRESS):
         posicion_triangulo[0] =  posicion_triangulo[0] + velocidad_triangulo
    #ARRIBA
    if key == glfw.KEY_UP and (action == glfw.PRESS):
         posicion_triangulo[1] =  posicion_triangulo[1] + velocidad_triangulo
    #ABAJO
    if key == glfw.KEY_DOWN and (action == glfw.PRESS):
         posicion_triangulo[1] =  posicion_triangulo[1] - velocidad_triangulo



def colisionando():
    colisionando = False
    for i in range(30):
        if (posicion_triangulo[0] + 0.04 >= posiciones_cuadrados[i][0] - 0.05 
            and posicion_triangulo[0] - 0.04 <= posiciones_cuadrados[i][0] + 0.1 
            and posicion_triangulo[1] + 0.04 >= posiciones_cuadrados[i][1] - 0.05 
            and posicion_triangulo[1] - 0.04 <= posiciones_cuadrados[i][1] + 0.05):
            colisionando = True 
    return colisionando

def draw_ranita():
    global posicion_triangulo
    glPushMatrix()
    glTranslatef(posicion_triangulo[0], posicion_triangulo[1],0.0)
    glScalef(0.5,0.5,0.0) 

    #Revisar colision
    if colisionando():
        glfw.set_window_should_close(window)
        glColor3f(1,0,0)
    else:
        glColor3f(98/255,198/255,0/255)

    #RANA
    glTranslatef(0.75,0.2,0.0)
    glBegin(GL_QUADS)

    glVertex3f(-0.76, -0.11, 0.0)
    glVertex3f(-0.76, -0.15, 0.0)
    glVertex3f(-0.80, -0.15, 0.0)
    glVertex3f(-0.80, -0.11, 0.0)

    glVertex3f(-0.74, -0.25, 0.0)
    glVertex3f(-0.74, -0.15, 0.0)
    glVertex3f(-0.82, -0.15, 0.0)
    glVertex3f(-0.82, -0.25, 0.0)

    glVertex3f(-0.72, -0.18, 0.0)
    glVertex3f(-0.72, -0.15, 0.0)
    glVertex3f(-0.84, -0.15, 0.0)
    glVertex3f(-0.84, -0.18, 0.0)

    glVertex3f(-0.72, -0.22, 0.0)
    glVertex3f(-0.72, -0.25, 0.0)
    glVertex3f(-0.84, -0.25, 0.0)
    glVertex3f(-0.84, -0.22, 0.0)

    glVertex3f(-0.72, -0.27, 0.0)
    glVertex3f(-0.72, -0.22, 0.0)
    glVertex3f(-0.74, -0.22, 0.0)
    glVertex3f(-0.74, -0.27, 0.0)

    glVertex3f(-0.82, -0.27, 0.0)
    glVertex3f(-0.82, -0.22, 0.0)
    glVertex3f(-0.84, -0.22, 0.0)
    glVertex3f(-0.84, -0.27, 0.0)

    glVertex3f(-0.82, -0.13, 0.0)
    glVertex3f(-0.82, -0.15, 0.0)
    glVertex3f(-0.84, -0.15, 0.0)
    glVertex3f(-0.84, -0.13, 0.0)

    glVertex3f(-0.72, -0.13, 0.0)
    glVertex3f(-0.72, -0.15, 0.0)
    glVertex3f(-0.74, -0.15, 0.0)
    glVertex3f(-0.74, -0.13, 0.0)
    glEnd()

    glPopMatrix()

#CARROS    
def draw_cuadrado():
    global posiciones_cuadrados


    for i in range(30):
        glPushMatrix()
        glTranslatef(posiciones_cuadrados[i][0], posiciones_cuadrados[i][1], 0.0)
        if direcciones_cuadrados[i]==2:
            glRotatef(180, 0, 0, 1)
            glBegin(GL_QUADS)
            
            glColor3f(234/255,129/255,25/255)
            glVertex3f(-0.05,0.04,0.0)
            glVertex3f(-0.03,0.04,0.0)
            glVertex3f(-0.03,-0.04,0.0)
            glVertex3f(-0.05,-0.04,0.0)

            glColor3f(234/255,129/255,25/255)
            glVertex3f(-0.03,0.01,0.0)
            glVertex3f(-0.01,0.01,0.0)
            glVertex3f(-0.01,-0.01,0.0)
            glVertex3f(-0.03,-0.01,0.0)

            glColor3f(234/255,129/255,25/255)
            glVertex3f(-0.01,0.03,0.0)
            glVertex3f(0.05,0.03,0.0)
            glVertex3f(0.05,-0.03,0.0)
            glVertex3f(-0.01,-0.03,0.0)

            glColor3f(234/255,129/255,25/255)
            glVertex3f(0.05,0.015,0.0)
            glVertex3f(0.065,0.015,0.0)
            glVertex3f(0.065,-0.015,0.0)
            glVertex3f(0.05,-0.015,0.0)

            glColor3f(234/255,129/255,25/255)
            glVertex3f(0.05,0.01,0.0)
            glVertex3f(0.1,0.01,0.0)
            glVertex3f(0.1,-0.01,0.0)
            glVertex3f(0.05,-0.01,0.0)

            glColor3f(99/255,156/255,247/255)
            glVertex3f(-0.005,0.01,0.0)
            glVertex3f(0.03,0.01,0.0)
            glVertex3f(0.03,-0.01,0.0)
            glVertex3f(-0.005,-0.01,0.0)

            #Llanta arriba trasera
            glColor3f(0,0,0)
            glVertex3f(-0.01,0.04,0.0)
            glVertex3f(0.015,0.04,0.0)
            glVertex3f(0.015,0.03,0.0)
            glVertex3f(-0.01,0.03,0.0)

            #Llanta abajo trasera
            glColor3f(0,0,0)
            glVertex3f(-0.01,-0.041,0.0)
            glVertex3f(0.015,-0.041,0.0)
            glVertex3f(0.015,-0.03,0.0)
            glVertex3f(-0.01,-0.03,0.0)

            #tubo llanta superior
            glColor3f(207/255,209/255,212/255)
            glVertex3f(0.09,0.03,0.0)
            glVertex3f(0.08,0.03,0.0)
            glVertex3f(0.08,0.01,0.0)
            glVertex3f(0.09,0.01,0.0)

            #tubo llanta inferior
            glColor3f(207/255,209/255,212/255)
            glVertex3f(0.09,-0.01,0.0)
            glVertex3f(0.08,-0.01,0.0)
            glVertex3f(0.08,-0.03,0.0)
            glVertex3f(0.09,-0.03,0.0)

            #Llanta abajo frontal
            glColor3f(0,0,0)
            glVertex3f(0.1,-0.041,0.0)
            glVertex3f(0.07,-0.041,0.0)
            glVertex3f(0.07,-0.03,0.0)
            glVertex3f(0.1,-0.03,0.0)

            #Llanta arriba trasera
            glColor3f(0,0,0)
            glVertex3f(0.1,0.04,0.0)
            glVertex3f(0.07,0.04,0.0)
            glVertex3f(0.07,0.03,0.0)
            glVertex3f(0.1,0.03,0.0)

            glEnd()
            
            glPopMatrix()
        else:
            glBegin(GL_QUADS)
            
            glColor3f(198/255,27/255,0/255)
            glVertex3f(-0.05,0.04,0.0)
            glVertex3f(-0.03,0.04,0.0)
            glVertex3f(-0.03,-0.04,0.0)
            glVertex3f(-0.05,-0.04,0.0)

            glColor3f(198/255,27/255,0/255)
            glVertex3f(-0.03,0.01,0.0)
            glVertex3f(-0.01,0.01,0.0)
            glVertex3f(-0.01,-0.01,0.0)
            glVertex3f(-0.03,-0.01,0.0)

            glColor3f(198/255,27/255,0/255)
            glVertex3f(-0.01,0.03,0.0)
            glVertex3f(0.05,0.03,0.0)
            glVertex3f(0.05,-0.03,0.0)
            glVertex3f(-0.01,-0.03,0.0)

            glColor3f(198/255,27/255,0/255)
            glVertex3f(0.05,0.015,0.0)
            glVertex3f(0.065,0.015,0.0)
            glVertex3f(0.065,-0.015,0.0)
            glVertex3f(0.05,-0.015,0.0)

            glColor3f(198/255,27/255,0/255)
            glVertex3f(0.05,0.01,0.0)
            glVertex3f(0.1,0.01,0.0)
            glVertex3f(0.1,-0.01,0.0)
            glVertex3f(0.05,-0.01,0.0)

            glColor3f(99/255,156/255,247/255)
            glVertex3f(-0.005,0.01,0.0)
            glVertex3f(0.03,0.01,0.0)
            glVertex3f(0.03,-0.01,0.0)
            glVertex3f(-0.005,-0.01,0.0)

            #Llanta arriba trasera
            glColor3f(0,0,0)
            glVertex3f(-0.01,0.04,0.0)
            glVertex3f(0.015,0.04,0.0)
            glVertex3f(0.015,0.03,0.0)
            glVertex3f(-0.01,0.03,0.0)

            #Llanta abajo trasera
            glColor3f(0,0,0)
            glVertex3f(-0.01,-0.041,0.0)
            glVertex3f(0.015,-0.041,0.0)
            glVertex3f(0.015,-0.03,0.0)
            glVertex3f(-0.01,-0.03,0.0)

            #tubo llanta superior
            glColor3f(207/255,209/255,212/255)
            glVertex3f(0.09,0.03,0.0)
            glVertex3f(0.08,0.03,0.0)
            glVertex3f(0.08,0.01,0.0)
            glVertex3f(0.09,0.01,0.0)

            #tubo llanta inferior
            glColor3f(207/255,209/255,212/255)
            glVertex3f(0.09,-0.01,0.0)
            glVertex3f(0.08,-0.01,0.0)
            glVertex3f(0.08,-0.03,0.0)
            glVertex3f(0.09,-0.03,0.0)

            #Llanta abajo frontal
            glColor3f(0,0,0)
            glVertex3f(0.1,-0.041,0.0)
            glVertex3f(0.07,-0.041,0.0)
            glVertex3f(0.07,-0.03,0.0)
            glVertex3f(0.1,-0.03,0.0)

            #Llanta arriba trasera
            glColor3f(0,0,0)
            glVertex3f(0.1,0.04,0.0)
            glVertex3f(0.07,0.04,0.0)
            glVertex3f(0.07,0.03,0.0)
            glVertex3f(0.1,0.03,0.0)

            glEnd()
            
            glPopMatrix()
            
def draw_cartel():
    glPushMatrix()
    glTranslatef(-.3,.43,0)

    glBegin(GL_POLYGON)
    glColor3f(221/255, 7/255, 7/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.05 * math.cos(angulo * math.pi / 180) , 0.045 * math.sin(angulo * math.pi / 180) -0, 0)
    glEnd()

    glPopMatrix()

def draw_arbol1():
    glPushMatrix()
    glTranslatef(.3,.42,0)
    glBegin(GL_POLYGON)
    glColor3f(66/255, 193/255, 42/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.1 * math.cos(angulo * math.pi / 180) , 0.065 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(66/255, 193/255, 42/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.065 * math.cos(angulo * math.pi / 180) , 0.09 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(40/255, 121/255, 24/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) +.03, 0.01 * math.sin(angulo * math.pi / 180) -.09, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(40/255, 121/255, 24/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) -.03, 0.01 * math.sin(angulo * math.pi / 180) -.01, 0)
    glEnd()
    
    glBegin(GL_POLYGON)
    glColor3f(40/255, 121/255, 24/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) +0.05, 0.01 * math.sin(angulo * math.pi / 180) -.03, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(40/255, 121/255, 24/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) -0.03, 0.01 * math.sin(angulo * math.pi / 180) -.05, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(40/255, 121/255, 24/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) -0.07, 0.01 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(40/255, 121/255, 24/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) +0.04, 0.01 * math.sin(angulo * math.pi / 180) -.06, 0)
    glEnd()
    glPopMatrix()

def draw_arbol2():
    glPushMatrix()
    glTranslatef(-.29,-.29,0)
    glBegin(GL_POLYGON)
    glColor3f(182/255, 204/255, 4/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.1 * math.cos(angulo * math.pi / 180) , 0.065 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(182/255, 204/255, 4/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.065 * math.cos(angulo * math.pi / 180) , 0.09 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(87/255, 95/255, 21/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) +.03, 0.01 * math.sin(angulo * math.pi / 180) -.09, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(87/255, 95/255, 21/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) -.03, 0.01 * math.sin(angulo * math.pi / 180) -.01, 0)
    glEnd()
    
    glBegin(GL_POLYGON)
    glColor3f(87/255, 95/255, 21/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) +0.05, 0.01 * math.sin(angulo * math.pi / 180) -.03, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(87/255, 95/255, 21/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) +0.03, 0.01 * math.sin(angulo * math.pi / 180) -.05, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(87/255, 95/255, 21/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) -0.02, 0.01 * math.sin(angulo * math.pi / 180) -.02, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(87/255, 95/255, 21/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.01 * math.cos(angulo * math.pi / 180) -0.08, 0.01 * math.sin(angulo * math.pi / 180) -.05, 0)
    glEnd()
    glPopMatrix()

def draw_mosca():
    global posicion_mosca
    glPushMatrix()
    glTranslatef(posicion_mosca[0], posicion_mosca[1], 0)
    glBegin(GL_POLYGON)
    glColor3f(31/255, 31/255, 31/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.02 * math.cos(angulo * math.pi / 180) , 0.025 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(147/255, 234/255, 249/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.025 * math.cos(angulo * math.pi / 180) +0.03, 0.010 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(147/255, 234/255, 249/255)
    for angulo in range(0, 359, 5):
        glVertex3f(0.025 * math.cos(angulo * math.pi / 180) -0.03, 0.010 * math.sin(angulo * math.pi / 180) -.08, 0)
    glEnd()
    glPopMatrix()

def draw_semaforos():
    #Semáforos banqueta arriba
    #Semaforo Izquierdo
    glBegin(GL_QUADS)
    glColor3f(84/255, 88/255, 89/255)
    glVertex3f(-0.85,0.31,0.0)
    glVertex3f(-0.9,0.31,0.0)
    glVertex3f(-0.9,0.37,0.0)
    glVertex3f(-0.85,0.37,0.0)

    #foco
    glColor3f(240/255, 242/255, 131/255)
    glVertex3f(-0.853,0.265,0.0)
    glVertex3f(-0.895,0.265,0.0)
    glVertex3f(-0.895,0.30,0.0)
    glVertex3f(-0.853,0.30,0.0)

    #tubo
    glColor3f(43/255, 45/255, 46/255)
    glVertex3f(-0.86,0.27,0.0)
    glVertex3f(-0.89,0.27,0.0)
    glVertex3f(-0.89,0.39,0.0)
    glVertex3f(-0.86,0.39,0.0)

    #Semáforo derecho
    glColor3f(84/255, 88/255, 89/255)
    glVertex3f(0.85,0.31,0.0)
    glVertex3f(0.9,0.31,0.0)
    glVertex3f(0.9,0.37,0.0)
    glVertex3f(0.85,0.37,0.0)

    #foco
    glColor3f(240/255, 242/255, 131/255)
    glVertex3f(0.853,0.265,0.0)
    glVertex3f(0.895,0.265,0.0)
    glVertex3f(0.895,0.30,0.0)
    glVertex3f(0.853,0.30,0.0)

    #tubo
    glColor3f(43/255, 45/255, 46/255)
    glVertex3f(0.86,0.27,0.0)
    glVertex3f(0.89,0.27,0.0)
    glVertex3f(0.89,0.39,0.0)
    glVertex3f(0.86,0.39,0.0)

    glEnd()

    #Semáforos banqueta abajo
    #Izquierdo
    glBegin(GL_QUADS)
    glColor3f(84/255, 88/255, 89/255)
    glVertex3f(-0.85,-0.33,0.0)
    glVertex3f(-0.9,-0.33,0.0)
    glVertex3f(-0.9,-0.39,0.0)
    glVertex3f(-0.85,-0.39,0.0)

    #foco
    glColor3f(240/255, 242/255, 131/255)
    glVertex3f(-0.853,-0.445,0.0)
    glVertex3f(-0.895,-0.445,0.0)
    glVertex3f(-0.895,-0.40,0.0)
    glVertex3f(-0.853,-0.40,0.0)

    #tubo
    glColor3f(43/255, 45/255, 46/255)
    glVertex3f(-0.86,-0.31,0.0)
    glVertex3f(-0.89,-0.31,0.0)
    glVertex3f(-0.89,-0.44,0.0)
    glVertex3f(-0.86,-0.44,0.0)

    #Derecho
    glColor3f(84/255, 88/255, 89/255)
    glVertex3f(0.85,-0.33,0.0)
    glVertex3f(0.9,-0.33,0.0)
    glVertex3f(0.9,-0.39,0.0)
    glVertex3f(0.85,-0.39,0.0)

    #foco
    glColor3f(240/255, 242/255, 131/255)
    glVertex3f(0.853,-0.445,0.0)
    glVertex3f(0.895,-0.445,0.0)
    glVertex3f(0.895,-0.40,0.0)
    glVertex3f(0.853,-0.40,0.0)

    #tubo
    glColor3f(43/255, 45/255, 46/255)
    glVertex3f(0.86,-0.31,0.0)
    glVertex3f(0.89,-0.31,0.0)
    glVertex3f(0.89,-0.44,0.0)
    glVertex3f(0.86,-0.44,0.0)

    glEnd()
    
def draw():
    draw_ranita()
    draw_cuadrado()
    draw_semaforos()
    draw_mosca()
    draw_arbol1()
    draw_arbol2()
    draw_cartel()

def background():

    #ground
    glBegin(GL_QUADS)
    glColor3f(61/255, 0/255, 198/255)
    glVertex3f(-1.0,2.0,0.0)
    glVertex3f(1.0,2.0,0.0)
    glVertex3f(1.0,-2.0,0.0)
    glVertex3f(-1.0,-2.0,0.0)
    glEnd()

    #Calle
    glBegin(GL_QUADS)
    glColor3f(92/255,92/255,92/255)
    glVertex3f(-1.0,0.9,0.0)
    glVertex3f(1.0,0.9,0.0)
    glVertex3f(1.0,-0.9,0.0)
    glVertex3f(-1.0,-0.9,0.0)
    glEnd()

    #Banqueta
    glBegin(GL_QUADS)
    glColor3f(184/255, 186/255, 186/255)
    glVertex3f(-1.0,-0.30,0.0)
    glVertex3f(1.0,-0.30,0.0)
    glVertex3f(1.0,-0.40,0.0)
    glVertex3f(-1.0,-0.40,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(184/255, 186/255, 186/255)
    glVertex3f(-1.0,0.30,0.0)
    glVertex3f(1.0,0.30,0.0)
    glVertex3f(1.0,0.40,0.0)
    glVertex3f(-1.0,0.40,0.0)
    glEnd()

    #Lineas calle
    glPushMatrix()
    glTranslatef(0,0,0)
    glBegin(GL_QUADS)
    glColor3f(255/255, 227/255, 11/255)
    glVertex3f(-1.0,0.025,0.0)
    glVertex3f(-0.8,0.025,0.0)
    glVertex3f(-0.8,-0.025,0.0)
    glVertex3f(-1.0,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 227/255, 11/255)
    glVertex3f(-0.5,0.025,0.0)
    glVertex3f(-0.3,0.025,0.0)
    glVertex3f(-0.3,-0.025,0.0)
    glVertex3f(-0.5,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 227/255, 11/255)
    glVertex3f(0.0,0.025,0.0)
    glVertex3f(0.2,0.025,0.0)
    glVertex3f(0.2,-0.025,0.0)
    glVertex3f(0.0,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 227/255, 11/255)
    glVertex3f(0.5,0.025,0.0)
    glVertex3f(0.7,0.025,0.0)
    glVertex3f(0.7,-0.025,0.0)
    glVertex3f(0.5,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 227/255, 11/255)
    glVertex3f(0.5,0.025,0.0)
    glVertex3f(0.7,0.025,0.0)
    glVertex3f(0.7,-0.025,0.0)
    glVertex3f(0.5,-0.025,0.0)
    glEnd()
    glPopMatrix()

    #Lineas calle
    glPushMatrix()
    glTranslatef(.1,-.67,0)
    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(-1.0,0.025,0.0)
    glVertex3f(-0.8,0.025,0.0)
    glVertex3f(-0.8,-0.025,0.0)
    glVertex3f(-1.0,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(-0.5,0.025,0.0)
    glVertex3f(-0.3,0.025,0.0)
    glVertex3f(-0.3,-0.025,0.0)
    glVertex3f(-0.5,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(0.0,0.025,0.0)
    glVertex3f(0.2,0.025,0.0)
    glVertex3f(0.2,-0.025,0.0)
    glVertex3f(0.0,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(0.5,0.025,0.0)
    glVertex3f(0.7,0.025,0.0)
    glVertex3f(0.7,-0.025,0.0)
    glVertex3f(0.5,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(0.5,0.025,0.0)
    glVertex3f(0.7,0.025,0.0)
    glVertex3f(0.7,-0.025,0.0)
    glVertex3f(0.5,-0.025,0.0)
    glEnd()
    glPopMatrix()

    #Lineas calle
    glPushMatrix()
    glTranslatef(.1,.67,0)
    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(-1.0,0.025,0.0)
    glVertex3f(-0.8,0.025,0.0)
    glVertex3f(-0.8,-0.025,0.0)
    glVertex3f(-1.0,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(-0.5,0.025,0.0)
    glVertex3f(-0.3,0.025,0.0)
    glVertex3f(-0.3,-0.025,0.0)
    glVertex3f(-0.5,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(0.0,0.025,0.0)
    glVertex3f(0.2,0.025,0.0)
    glVertex3f(0.2,-0.025,0.0)
    glVertex3f(0.0,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(0.5,0.025,0.0)
    glVertex3f(0.7,0.025,0.0)
    glVertex3f(0.7,-0.025,0.0)
    glVertex3f(0.5,-0.025,0.0)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(255/255, 255/255, 255/255)
    glVertex3f(0.5,0.025,0.0)
    glVertex3f(0.7,0.025,0.0)
    glVertex3f(0.7,-0.025,0.0)
    glVertex3f(0.5,-0.025,0.0)
    glEnd()
    glPopMatrix()

    #Alcantarillas
    glBegin(GL_POLYGON)
    glColor3f(143/255, 145/255, 148/255)
    for angulo in range(0,359,5):
        glVertex3f(0.06 * math.cos(angulo * math.pi / 180) - 0.3, 0.06 * math.sin(angulo * math.pi/180) + 0.58, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(175/255, 176/255, 179/255)
    for angulo in range(0,359,5):
        glVertex3f(0.05 * math.cos(angulo * math.pi / 180) - 0.3, 0.05 * math.sin(angulo * math.pi/180) + 0.58, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(143/255, 145/255, 148/255)
    for angulo in range(0,359,5):
        glVertex3f(0.06 * math.cos(angulo * math.pi / 180) + 0.3, 0.06 * math.sin(angulo * math.pi/180) - 0.58, 0)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0/255, 0/255, 0/255)
    for angulo in range(0,359,5):
        glVertex3f(0.05 * math.cos(angulo * math.pi / 180) + 0.3, 0.05 * math.sin(angulo * math.pi/180) - 0.58, 0)
    glEnd()



def main():
    global window

    width = 600
    height = 700

    if not glfw.init():
        return

    window = glfw.create_window(width, height, "Frogger", None, None)

    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glewExperimental = True

    if glewInit() != GLEW_OK:
        print("No se pudo inicializar GLEW")
        return

    version = glGetString(GL_VERSION)
    print(version)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glClearColor(0.7,0.7,0.7,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        background()
        actualizar()
        draw()

        glfw.poll_events()

        glfw.swap_buffers(window)

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()