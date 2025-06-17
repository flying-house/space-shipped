import pygame #type: ignore
import sys

from game.ship import Ship
from game.constants import *
from engine.hud import HUD

def main():
    pygame.init()

    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption("Space Shipped")
    clock = pygame.time.Clock()

    ship = Ship(screenW//2, screenH//2)
    hud = HUD()
    playerMoney = 0

    running = True
    while running:
        dt = clock.get_time() / 1000.0 # seconds

        # I realize I need to create an input handler separate from main here
        # and just need to figure out how best to do it. Passing all commands
        # in via update() is a bit silly, I know, but for now it works to test
        keys = pygame.key.get_pressed()
        thrustF = keys[pygame.K_w]
        thrustR = keys[pygame.K_s] 
        rotateL = keys[pygame.K_a]
        rotateR = keys[pygame.K_d]
        slewL = keys[pygame.K_q]
        slewR = keys[pygame.K_e]
        ship.update(dt, thrustF, thrustR, rotateL, rotateR, slewL, slewR)

        # sneaky refuel command for testing
        if keys[pygame.K_p]:    
            if ship.fuel < ship.maxFuel:
                ship.fuel = ship.maxFuel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((5, 10, 50))
        ship.draw(screen)
        hud.draw(screen, ship, playerMoney)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
