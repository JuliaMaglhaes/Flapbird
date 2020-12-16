import pygame
import random
import itens
from pygame.locals import *

#Variaveis
width = 800
height = 600
game = True
cair = False #caso ele caia o jogo acaba
g_over= True
mover = 1
acelerar = 4
asas_animacao = 0
vel_y = 0
pontos = 0
record = 0
cano = []

pygame.init()
windows = pygame.display.set_mode((width, height))

#Imagens do jogo
imagem1 = pygame.image.load("img/flap1.png")
imagem2 = pygame.image.load("img/flap2.png")
chao = pygame.image.load("img/chao.png")
tubo = pygame.image.load("img/tubo.png")
background = pygame.image.load("img/background.png")

#Objetos de cena
play = itens.Itens(windows, 200, height / 3, 50, 50, imagem1, 0)
fundo1= itens.Itens(windows, 0, 210, 0, 0, background, 0)
fundo2 = itens.Itens(windows, width, 210, 0, 0, background, 0)
chao1 = itens.Itens(windows, 0, 466, 0, 0, chao, 0)
chao2 = itens.Itens(windows, width, 466, 0, 0, chao, 0)

for i in range(2):
    cano.append([0] * 4)

for i in range(4):
    cano[0][i] = itens.Itens(windows, i*210, -100, 87, 310, tubo, 0 )
    cano[1][i] = itens.Itens(windows, i*210, 400, 87, 310, tubo, 0 )


def restaurar():
    global vel_y, acelerar, cair, pontos

    for i in range(4):
        cano[0][i].x = width + i *220
        cano[1][i].x = width + i *220
        visible = random.randint(0, 1)
        cano[0][i].visible = visible
        cano[1][i].visible = visible
        cano_y = random.randint(0,9) * -(cano[0][0].h/10)
        cano[0][i].y = cano_y
        cano[1][i].y = cano_y + 470
        cano[1][i].r = 180 #inverrter cano
    
    play.y = height/3
    vel_y =0
    cair = False
    pontos = 0

def graficos ():
    global asas_animacao

    pygame.display.update()
    pygame.time.delay(10)
    windows.fill(0x3C2EE)
    

    #Animacao asas
    asas_animacao += 1
    if asas_animacao >10:
        play.img = imagem1
    else:
        play.img = imagem2
    if asas_animacao >20:
        asas_animacao = 0

    #Cenario movimento
    if fundo1.x < -width:
        fundo1.x = 0
        fundo2.x = width

    fundo1.x -= mover * 1
    fundo2.x -= mover * 1

    fundo1.mostrar()
    fundo2.mostrar()

    #cano
    for i in range(4):
        cano[0][i].mostrar()
        cano[1][i].mostrar()
        cano[0][i].x -= mover *acelerar
        cano[1][i].x -= mover * acelerar

        if cano[0][i].x < -cano[0][0].w:
            visible = random.randint(0, 1)
            cano[0][i].visible = visible
            cano[1][i].visible = visible
            cano_y = random.randint (0, 9) * -(cano[0][0].h/10)
            cano[0][i].y = cano_y
            cano[1][i].y = cano_y + 470
            cano[0][i].x = width
            cano[1][i].x = width

    #Chao
    if chao1.x < -width:
        chao1.x = 0
        chao2.x = width
    
    chao1.x -= mover *5
    chao2.x -=mover * 5
    chao1.mostrar()
    chao2.mostrar()

    #player
    play.mostrar()

def controle():
    global g_over, vel_y, mover, cair

    mover = not g_over
    vel_y += mover
    play.y += mover * vel_y
    play.r = mover * (-vel_y)*3

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
        if event.type == KEYDOWN and event.key == K_SPACE and g_over:
            g_over = False
            restaurar()
        if event.type == pygame.MOUSEBUTTONDOWN and not cair:
            vel_y = mover * -12

    return True

while game:
    graficos()
    game = controle()