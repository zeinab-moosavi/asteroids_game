import pygame
from circleshape import CircleShape

class Bomb(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 10)  # Small bomb radius
        self.fuse_timer = 3.0  # Explodes after 3 seconds
        self.blast_radius = 150  # How far the explosion reaches
        self.exploded = False
    def draw(self, screen):
        # Bomb flashes faster as it's about to explode
        if int(self.fuse_timer * 5) % 2 == 0:
            color = "red"
        else:
            color = "orange"
        pygame.draw.circle(screen, color, self.position, self.radius)
    def update(self, dt):
        self.fuse_timer -= dt
        if self.fuse_timer <= 0:
            self.exploded = True
    def get_asteroids_in_blast(self, asteroids):
        """Return all asteroids within blast radius."""
        hit_asteroids = []
        for asteroid in asteroids:
            distance = self.position.distance_to(asteroid.position)
            if distance <= self.blast_radius + asteroid.radius:
                hit_asteroids.append(asteroid)
        return hit_asteroids

class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, max_radius):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.radius = 10
        self.max_radius = max_radius
        self.growth_speed = 300
    def draw(self, screen):
        pygame.draw.circle(screen, "orange", self.position, int(self.radius), 3)
        pygame.draw.circle(screen, "yellow", self.position, int(self.radius * 0.7), 2)
    def update(self, dt):
        self.radius += self.growth_speed * dt
        if self.radius >= self.max_radius:
            self.kill()
