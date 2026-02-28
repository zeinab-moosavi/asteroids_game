from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_FRICTION, PLAYER_ACCELERATION, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from shot import Shot
from weapon import Blaster
from bomb import Bomb
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.invincible_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.weapon = Blaster()
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.speed_multiplier = 1.0
        self.bomb_count = 3  # Start with 3 bombs
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        # Draw shield bubble when active
        if self.shield_active:
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 10, 2)
        # Speed boost - draw engine flame behind ship
        if self.speed_boost_active:
            backward = pygame.Vector2(0, -1).rotate(self.rotation)
            flame_start = self.position + backward * self.radius
            flame_end = self.position + backward * (self.radius + 20)
            pygame.draw.line(screen, "orange", flame_start, flame_end, 3)
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    def update(self, dt):
        self.weapon.update(dt)
        #Handle Timers
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        # Handle shield timer
        if self.shield_timer > 0:
            self.shield_timer -= dt
        if self.shield_timer <= 0:
            self.shield_active = False
        # Handle speed boost timer
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
        if self.speed_boost_timer <= 0:
            self.speed_boost_active = False
            self.speed_multiplier = 1.0
        # Handle Rotation (Input)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
           self.rotate(dt)
        # Handle Acceleration (Input)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if keys[pygame.K_w]:
            self.velocity += forward * PLAYER_ACCELERATION * self.speed_multiplier * dt
        if keys[pygame.K_s]:
            self.velocity -= forward * PLAYER_ACCELERATION * self.speed_multiplier * dt
        # 4. Handle Physics (Movement and Friction)
        self.velocity *= (1 - PLAYER_FRICTION * dt)
        # Update the actual position
        self.position += self.velocity * dt
        # Wrap around screen
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
        if keys[pygame.K_SPACE]:
            self.shoot()
    def shoot(self):
        if self.weapon.can_fire():
            self.weapon.fire(self.position, self.rotation)
    def make_invincible(self, duration=2):
        self.invincible_timer = duration
    def is_invincible(self):
        return self.invincible_timer > 0
    def switch_weapon(self, new_weapon):
        self.weapon = new_weapon
    def point_in_triangle(self, point):
        """Check if a point is inside the player's triangle."""
        a, b, c = self.triangle()
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
        d1 = sign(point, a, b)
        d2 = sign(point, b, c)
        d3 = sign(point, c, a)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)
    def line_circle_intersect(self, circle_pos, circle_radius):
        """Check if a circle intersects any of the triangle's edges."""
        a, b, c = self.triangle()
        edges = [(a, b), (b, c), (c, a)]
        for line_start, line_end in edges:
            # Vector from line start to end
            line_vec = line_end - line_start
            # Vector from line start to circle center
            to_circle = circle_pos - line_start
            # Project circle center onto the line
            line_length_sq = line_vec.length_squared()
            if line_length_sq == 0:
                # Line is a point
                if to_circle.length() <= circle_radius:
                    return True
                continue
            # How far along the line is the closest point (0 to 1)
            t = max(0, min(1, to_circle.dot(line_vec) / line_length_sq))
            # Find the closest point on the line segment
            closest_point = line_start + line_vec * t
            # Check if that point is within the circle's radius
            distance = (circle_pos - closest_point).length()
            if distance <= circle_radius:
                return True
        return False
    def collides_with(self, other):
        """Check if this player's triangle collides with a circular object."""
        if self.point_in_triangle(other.position):
            return True
        if self.line_circle_intersect(other.position, other.radius):
            return True
        return False
    def activate_shield(self, duration=5):
        self.shield_active = True
        self.shield_timer = duration

    def has_shield(self):
        return self.shield_active
    def activate_speed_boost(self, duration=5):
        self.speed_boost_active = True
        self.speed_boost_timer = duration
        self.speed_multiplier = 2.0  # Double speed

    def has_speed_boost(self):
        return self.speed_boost_active
    def drop_bomb(self):
        if self.bomb_count > 0:
            self.bomb_count -= 1
            Bomb(self.position.x, self.position.y)
