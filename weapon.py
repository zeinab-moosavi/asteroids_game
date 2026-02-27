from shot import Shot
import pygame
class Weapon:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.timer = 0

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt

    def can_fire(self):
        return self.timer <= 0

    def fire(self, position, rotation):
        self.timer = self.cooldown
        # This will be overridden by specific weapon types
        pass
class Blaster(Weapon):
    def __init__(self):
        # Fire once every 0.3 seconds
        super().__init__(0.3)

    def fire(self, position, rotation):
        super().fire(position, rotation)
        shot = Shot(position.x, position.y, 5)
        shot.velocity = pygame.Vector2(0, 1).rotate(rotation) * 500
        print("Blaster fired!")
class SpreadShot(Weapon):
    def __init__(self):
        # Fire once every 0.6 seconds (slower but more powerful)
        super().__init__(0.6)

    def fire(self, position, rotation):
        super().fire(position, rotation)
        angles = [rotation - 20, rotation, rotation + 20]
        for angle in angles:
            shot = Shot(position.x, position.y, 4)
            shot.velocity = pygame.Vector2(0, 1).rotate(angle) * 400
        print("SpreadShot fired!")
