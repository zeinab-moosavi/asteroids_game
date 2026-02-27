from circleshape import CircleShape
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, POINTS_SPLIT, POINTS_DESTROY, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import random
from score import Score
from explosion import ExplosionRing
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.rotation_speed = random.uniform(-100, 100)
        # Generate random vertex offsets once at creation
        self.num_vertices = random.randint(8, 12)
        # Each vertex has a random distance multiplier (0.7 to 1.3 of radius)
        self.vertex_offsets = [
            random.uniform(0.7, 1.3) for _ in range(self.num_vertices)
        ]
    def get_vertices(self):
        """Generate the lumpy polygon vertices."""
        vertices = []
        angle_step = 360 / self.num_vertices
        for i in range(self.num_vertices):
            angle = i * angle_step + self.rotation
            distance = self.radius * self.vertex_offsets[i]
            # Create a vector pointing outward at this angle
            direction = pygame.Vector2(0, 1).rotate(angle)
            vertex = self.position + direction * distance
            vertices.append(vertex)
        return vertices
    def draw(self, surface):
        pygame.draw.polygon(surface, "white", self.get_vertices(), LINE_WIDTH)
    def update(self, dt):
        self.position += self.velocity * dt
        # Wrap around screen
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.rotation += self.rotation_speed * dt
    def split(self, score):
        ExplosionRing(self.position.x, self.position.y, self.radius * 2)
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            score.add_points(POINTS_DESTROY)
            return
        log_event("asteroid_split")
        score.add_points(POINTS_SPLIT)
        new_redius = self.radius - ASTEROID_MIN_RADIUS
        fisrt_asteroid = Asteroid(self.position.x, self.position.y, new_redius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_redius)
        fisrt_asteroid.velocity = self.velocity.rotate(random.uniform(20, 50)) * 1.2
        second_asteroid.velocity = self.velocity.rotate(-(random.uniform(20, 50))) * 1.2
