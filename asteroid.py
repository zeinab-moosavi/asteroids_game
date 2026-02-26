from circleshape import CircleShape
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, POINTS_SPLIT, POINTS_DESTROY
import pygame
import random
from score import Score
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.position, self.radius, LINE_WIDTH)
    def update(self, dt):
        self.position += self.velocity * dt 
    def split(self, score):
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
