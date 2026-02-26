from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_FRICTION, PLAYER_ACCELERATION,  PLAYER_SHOOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from shot import Shot
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.invincible_timer = 0
        self.velocity = pygame.Vector2(0, 0)
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    def update(self, dt):
        # 1. Handle Timers
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        self.shot_cooldown_timer -= dt
        # 2. Handle Rotation (Input)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
           self.rotate(dt)
        # 3. Handle Acceleration (Input)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if keys[pygame.K_w]:
            self.velocity += forward * PLAYER_ACCELERATION * dt
        if keys[pygame.K_s]:
            self.velocity -= forward * PLAYER_ACCELERATION * dt
        # 4. Handle Physics (Movement and Friction)
        self.velocity *= (1 - PLAYER_FRICTION * dt)
        # Update the actual position
        self.position += self.velocity * dt
        # Wrap around screen
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown_timer <= 0:
                self.shot_cooldown_timer =  PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
    def shoot(self):
        shot = Shot(self.position.x, self.position.y , SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    def make_invincible(self, duration=2):
        self.invincible_timer = duration
    def is_invincible(self):
        return self.invincible_timer > 0
