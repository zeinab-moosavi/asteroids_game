import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from powerup import ShieldPowerUp
class PowerUpSpawner(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)
        self.spawn_timer = 0
        self.spawn_interval = 15  # Spawn every 15 seconds
    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Random position on screen
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            ShieldPowerUp(x, y)
