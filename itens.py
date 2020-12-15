import pygame

class Itens:
    def __init__(self, windows, x, y, w, h, img, r):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.visible = True
        self.img = img
        self.windows = windows

    def mostrar (self):
        image = pygame.transform.rotate(self.img, self.r)
        if self.visible:
            self.windows.blit(image, (self.x, self.y))