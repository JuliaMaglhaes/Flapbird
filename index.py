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

def colisao(a, b):
    return a.x + a.w > b.x and a.x < b.x + b.w and a.y + a.h > b.y and a.y < b.y + b.h


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

def gamee():
    global g_over, mover, asas_animacao, cair, pontos, record

    for i in range(2):
        for j in range(4):
            if colisao(cano[i][j], play) and cano[i][j].visible:
                cair = True
            if not i and 200 < cano[i][j].x < 205 and cano[i][j].visible and not g_over:
                pontos = pontos + 1
                if play.y < cano[i][j].y:
                    cair= True
    if play.y > chao1.y -play.h:
        g_over = True
        play.r = -90
        asas_animacao = 0
        cair = True

def textos():
    global pontos, record

    if pontos> record:
        record = pontos

    if g_over and cair:
        font = pygame.font.SysFont("arial", 36, 1) #preciso informar uma fonte ao chamar 
        pygame.draw.rect(windows, 0x543847, [300,100,190,200], 10)
        pygame.draw.rect(windows, 0xDED895, [305,104,180,190])
        txt = font.render("Recorde", 0, (255, 127, 39))
        windows.blit(txt, (310, 110))
        txt = font.render(str(record), 0, (255, 127, 39))
        windows.blit(txt, (380, 146))
        txt = font.render("Pontos", 0, (255, 127, 39))
        windows.blit(txt, (310, 184))
        txt = font.render(str(pontos), 0, (255, 127, 39))
        windows.blit(txt, (380, 220))
        txt = font.render("Pressione para jogar", 0, (255, 127, 39))
        windows.blit(txt, (350, 530))
    else:
        font = pygame.font.SysFont("arial black", 35)
        txt = font.render(str(pontos), 0, (255, 127, 39), 0x11d1E0)
        windows.blit(txt, (380, 146))

restaurar()

while game:
    gamee()
    textos()
    graficos()
    game = controle()