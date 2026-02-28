import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from shot import Shot
from score import Score
from asteroidField import AsteroidField
from lives import Lives
from weapon import Blaster, SpreadShot
from explosion import ExplosionRing
import sys
from powerup import ShieldPowerUp, SpeedPowerUp
from powerupSpawner import PowerUpSpawner
from bomb import Bomb, BombExplosion
from bomb_counter import BombCounter
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawables)
    Score.containers = (drawables, updatable)
    Lives.containers = (drawables, updatable)
    ExplosionRing.containers = (updatable, drawables)
    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, updatable, drawables)
    Player.containers = (updatable, drawables)
    ShieldPowerUp.containers = (powerups, updatable, drawables)
    SpeedPowerUp.containers = (powerups, updatable, drawables)
    PowerUpSpawner.containers = (updatable)
    Bomb.containers = (bombs, updatable, drawables)
    BombExplosion.containers = (updatable, drawables)
    BombCounter.containers = (updatable, drawables)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    bomb_counter = BombCounter(player)
    asteroid_field = AsteroidField()
    score = Score()
    lives = Lives()
    powerup_spawner = PowerUpSpawner()
    background = pygame.image.load("black.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.switch_weapon(Blaster())
                if event.key == pygame.K_2:
                    player.switch_weapon(SpreadShot())
                if event.key == pygame.K_b:
                    player.drop_bomb()
        #  screen.fill("black")
        screen.blit(background, (0, 0))
        for drawable in drawables:
            drawable.draw(screen) 
        updatable.update(dt)
        for asteroid  in asteroids:
            if player.collides_with(asteroid) and not player.is_invincible() and not player.has_shield():
                log_event("player_hit")
                lives.lose_one()
                if lives.is_alive():
                    # Respawn player at center
                    player.position.x = SCREEN_WIDTH / 2
                    player.position.y = SCREEN_HEIGHT / 2
                    player.velocity.x = 0
                    player.velocity.y = 0
                    player.make_invincible(2)
                else:
                    print("Game over!")
                    sys.exit()
            for shot  in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split(score)
        for powerup in powerups:
            if player.collides_with(powerup):
                if isinstance(powerup, ShieldPowerUp):
                    player.activate_shield(5)
                elif isinstance(powerup, SpeedPowerUp):
                    player.activate_speed_boost(5)
                powerup.kill()
        for bomb in bombs:
            if bomb.exploded:
                BombExplosion(bomb.position.x, bomb.position.y, bomb.blast_radius)
                # Destroy all asteroids in blast radius
                for asteroid in bomb.get_asteroids_in_blast(asteroids):
                     asteroid.split(score)
                bomb.kill()
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()
