import pygame

class ExplosionRing(pygame.sprite.Sprite):
    def __init__(self, x, y, max_radius=50):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.radius = 5  # Starting size
        self.max_radius = max_radius
        self.growth_speed = 150  # Pixels per second
    
    def update(self, dt):
        self.radius += self.growth_speed * dt
        if self.radius >= self.max_radius:
            self.kill()
    
    def draw(self, screen):
        # Calculate opacity based on how expanded the ring is
        # Fades out as it grows
        alpha = int(255 * (1 - self.radius / self.max_radius))
        pygame.draw.circle(screen, (255, 100, 0), self.position, int(self.radius), 2)
