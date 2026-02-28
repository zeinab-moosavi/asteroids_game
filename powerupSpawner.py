import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from powerup import ShieldPowerUp, SpeedPowerUp, BombPowerUp
class PowerUpSpawner(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)
        self.spawn_timer = 0
        self.spawn_interval = 15  # Spawn every 15 seconds
    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            # Randomly choose which power-up to spawn
            choice = random.randint(1, 3)
            if choice == 1:
                ShieldPowerUp(x, y)
            elif choice == 2:
                SpeedPowerUp(x, y)
            else:
                BombPowerUp(x, y)
