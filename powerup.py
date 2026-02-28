import pygame
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import random

class ShieldPowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 15)
    def draw(self, screen):
        # Draw a blue circle with a smaller circle inside
        pygame.draw.circle(screen, "cyan", self.position, self.radius, 2)
        pygame.draw.circle(screen, "blue", self.position, self.radius // 2)

    def update(self, dt):
        pass  # Power-up just sits there waiting to be collected
class SpeedPowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 15)
    def draw(self, screen):
        # Draw as yellow/orange to distinguish from shield
        pygame.draw.circle(screen, "yellow", self.position, self.radius, 2)
        pygame.draw.circle(screen, "orange", self.position, self.radius // 2)
    def update(self, dt):
        pass
