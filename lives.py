import pygame

class Lives(pygame.sprite.Sprite):
    def __init__(self, starting_lives=3):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.count = starting_lives
    
    def lose_one(self):
        self.count -= 1
    
    def is_alive(self):
        return self.count > 0
    
    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Lives: {self.count}", True, (255, 255, 255))
        screen.blit(text, (10, 50))  # Below the score
    
    def update(self, dt):
        pass
