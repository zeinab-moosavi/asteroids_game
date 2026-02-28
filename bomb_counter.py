import pygame

class BombCounter(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(self.containers)
        self.player = player
        self.font = pygame.font.Font(None, 36)
    def draw(self, screen):
        text = self.font.render(f"Bombs: {self.player.bomb_count}", True, "red")
        screen.blit(text, (10, 90))
    def update(self, dt):
        pass
