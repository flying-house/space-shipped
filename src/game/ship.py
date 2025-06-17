import pygame #type: ignore
import math
import json


class Ship:
    def __init__(self, x, y):
        with open("src/data/ships.json") as s:
            cfgShip = json.load(s)["basicShip"]
        self.name = cfgShip["name"]
        self.engine = cfgShip["engine"]

        with open("src/data/engines.json") as e:
            cfgEng = json.load(e)[self.engine]

        self.hdg = 0
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.angularVelocity = 0

        self.thrust = cfgEng["thrust"]
        self.engBurn = False
        self.revBurn = False
        self.engCost = cfgEng["fuelBurn"]
        self.length = cfgShip["length"]
        self.fuel = cfgShip["maxFuel"] // 2
        self.maxFuel = cfgShip["maxFuel"]
        self.massEmpty = cfgShip["mass"] + cfgEng["mass"]
        self.mass = self.massEmpty + self.fuel

        # turnRate in deg/s
        # TODO: MOI-based rate calc, ?angular momentum
        self.turnRate = cfgShip["turnRate"]
        self.turnCost = cfgShip["turnCost"]
        self.revThrust = cfgShip["revThrust"]
        self.revCost = cfgShip["revCost"]

    def update(self, dt, thrustFwd, thrustRev, rotateL, rotateR):
        self.engBurn = thrustFwd
        self.revBurn = thrustRev

        if rotateL:
            self.angularVelocity = -self.turnRate
            turnFuel = dt * self.turnCost
        elif rotateR:
            self.angularVelocity = self.turnRate
            turnFuel = dt * self.turnCost
        else:
            self.angularVelocity = 0
            turnFuel = 0

        burnFuel = 0
        thrustVector = pygame.Vector2(0, 0)

        if self.engBurn:
            thrustVector = pygame.Vector2(0, -self.thrust)
            burnFuel += dt * self.engCost
        if self.revBurn:
            thrustVector = pygame.Vector2(0, self.thrust)
            burnFuel += dt * self.revCost

        thrustVector.rotate_ip(self.hdg)
        self.velocity += (thrustVector * dt / self.mass) * 1000
        self.pos += dt * self.velocity
        self.hdg += dt * self.angularVelocity
        self.fuel -= (burnFuel + turnFuel)
        
    def draw(self, screen):
        shipPoints = [
            (0, -self.length),
            (-self.length//3, self.length//2),
            (self.length//3, self.length//2)
        ]
        rotatedPoints = []
        angleRad = math.radians(self.hdg)
        
        for px, py in shipPoints:
            rotatedX = px * math.cos(angleRad) - py * math.sin(angleRad)
            rotatedY = px * math.sin(angleRad) + py * math.cos(angleRad)
            
            finalX = rotatedX + self.pos.x
            finalY = rotatedY + self.pos.y
            rotatedPoints.append((finalX, finalY))
        
        pygame.draw.polygon(screen, (255, 255, 255), rotatedPoints)