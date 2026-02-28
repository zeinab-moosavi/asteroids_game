import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.value = 0
    def add_points(self, points):  # Renamed from add()
        self.value += points
    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.value}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
    def update(self, dt):
        pass
