import pygame #type: ignore
import math
import json


class Ship:
    def __init__(self, x, y):
        with open("src/data/ships.json") as s:
            cfgShip = json.load(s)["basicShip"]

        self.name = cfgShip["name"]
        self.engine = cfgShip["engine"]
        # can't use following open statement until engine name is fetched
        # unsure how to do this when eventually selecting ship & engine
        # from stored/saved gamestate data instead of hardcoded value
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
        self.engVectoring = cfgEng["vectoring"]
        self.length = cfgShip["length"]
        self.fuel = cfgShip["maxFuel"] // 8
        self.maxFuel = cfgShip["maxFuel"]
        self.massEmpty = cfgShip["mass"] + cfgEng["mass"]
        self.cargo = 0 # placeholder
        self.mass = self.massEmpty + self.fuel + self.cargo

        # turnRate in deg/s
        # TODO: MOI-based rate calc, ?angular momentum
        self.turnRate = cfgShip["turnRate"]
        self.turnCost = cfgShip["turnCost"]
        self.revThrust = cfgShip["revThrust"]
        self.revCost = cfgShip["revCost"]

    def update(self, dt, thrustFwd, thrustRev, rotateL, rotateR, slewL, slewR):
        self.engBurn = thrustFwd
        self.revBurn = thrustRev
        self.slewL = slewL
        self.slewR = slewR

        burnFuel, turnFuel, slewFuel = 0, 0, 0
        thrustVector = pygame.Vector2(0, 0)
        slewVector = pygame.Vector2(0, 0)

        if self.fuel > 0:
            if self.engBurn:
                thrustVector = pygame.Vector2(0, -self.thrust)
                burnFuel += dt * self.engCost
            if self.revBurn:
                thrustVector = pygame.Vector2(0, self.revThrust)
                burnFuel += dt * self.revCost

            if self.slewL:
                slewVector = pygame.Vector2(-self.revThrust // 2, 0)
                slewFuel += dt * self.revCost // 3
            elif self.slewR:
                slewVector = pygame.Vector2(self.revThrust // 2, 0)
                slewFuel += dt * self.revCost // 3
            else:
                self.slewVector = pygame.Vector2(0, 0)

            if rotateL and not thrustFwd:
                self.angularVelocity = -self.turnRate
                turnFuel = dt * self.turnCost
            elif rotateL and thrustFwd:
                # multiply steering by engine vectoring scalar
                thrustVectoredRate = self.turnRate * self.engVectoring
                self.angularVelocity = -thrustVectoredRate
                turnFuel = dt * self.turnCost
            elif rotateR and not thrustFwd:
                self.angularVelocity = self.turnRate
                turnFuel = dt * self.turnCost
            elif rotateR and thrustFwd:
                # multiply steering by engine vectoring scalar
                thrustVectoredRate = self.turnRate * self.engVectoring
                self.angularVelocity = thrustVectoredRate
                turnFuel = dt * self.turnCost
            else:
                self.angularVelocity = 0
        else:
            self.fuel = 0

        thrustVector.rotate_ip(self.hdg)
        slewVector.rotate_ip(self.hdg)
        self.velocity += (thrustVector * dt / self.mass) * 1000
        self.velocity += (slewVector * dt / self.mass) * 1000
        self.pos += dt * self.velocity
        self.hdg += dt * self.angularVelocity
        self.fuel -= (burnFuel + turnFuel + slewFuel)
        self.mass = self.massEmpty + self.fuel + self.cargo
        
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