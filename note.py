import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("assets/note.png").convert_alpha()
        self.image_size = self.image.get_size()
        self.zoom = 3
        self.image = pygame.transform.scale(self.image, (self.image_size[0] * self.zoom, self.image_size[1] * self.zoom))
        self.image_rect = self.image.get_rect()
        self.scroll_speed = 0

    def move(self, direc, val):
        if direc == "down":
            self.image_rect.y -= val
            print("asd")