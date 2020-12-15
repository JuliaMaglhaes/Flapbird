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
        if self.visible:
            self.windows.blit(self.img, (self.x, self.y))