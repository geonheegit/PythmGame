import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, key):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/note.png").convert_alpha()
        self.image_size = self.image.get_size()
        self.zoom = 3
        self.image = pygame.transform.scale(self.image, (self.image_size[0] * self.zoom, self.image_size[1] * self.zoom))
        self.rect = self.image.get_rect()
        self.scroll_speed = 6
        self.key = key

        if key == "S":
            self.rect.x = 70
        if key == "D":
            self.rect.x = 170
        if key == "K":
            self.rect.x = 270
        if key == "L":
            self.rect.x = 370

    def update(self, HEIGHT):
        self.rect.y += self.scroll_speed