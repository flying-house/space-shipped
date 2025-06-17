import pygame #type: ignore

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 16)
        self.smallFont = pygame.font.Font(None, 12)

    def draw(self, screen, ship, money=0):
        speed = ship.velocity.magnitude()
        heading = int(ship.hdg % 360)

        hudLines = [
            f"Pos: ({int(ship.pos.x)}, {int(ship.pos.y)})",
            f"Speed: {speed:.1f} m/s",
            f"Heading: {heading}°", 
            f"Fuel: {int(ship.fuel)}/{int(ship.maxFuel)}",
            f"Money: ${money}",
        ]
        hudHeight = len(hudLines) * 25 + 10
        pygame.draw.rect(screen, (0, 0, 0, 128), (10, 10, 250, hudHeight))
        
        for i, line in enumerate(hudLines):
            color = (255, 255, 255)
            if "Fuel:" in line and ship.fuel < (ship.maxFuel * 0.07):
                color = (255, 100, 100)  # Red when low fuel
                
            text = self.font.render(line, True, color)
            screen.blit(text, (15, 15 + i * 25))