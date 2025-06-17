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
        self.engBurn = False
        self.revBurn = False
        self.thrust = cfgEng["thrust"]
        self.engCost = cfgEng["fuelBurn"]
        self.engVectoring = cfgEng["vectoring"]
        self.length = cfgShip["length"]
        self.fuel = cfgShip["maxFuel"] // 8
        self.maxFuel = cfgShip["maxFuel"]
        self.massEmpty = cfgShip["mass"] + cfgEng["mass"]
        self.cargo = 0 # TODO: replace placeholder with a getCargoMass() (below)
        self.mass = self.massEmpty + self.fuel + self.cargo
        # TODO: turnRate could be MOI-based rate calc
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
        

        # these seem like a good candidate for their own method within Ship
        # or possibly the physics components offloaded to a src/engine/ module?
        if self.fuel > 0:
            # main engine thrust handling
            if self.engBurn:
                thrustVector = pygame.Vector2(0, -self.thrust)
                burnFuel += dt * self.engCost
            if self.revBurn:
                thrustVector = pygame.Vector2(0, self.revThrust)
                burnFuel += dt * self.revCost

            # slow RCS venting
            if self.slewL:
                slewVector = pygame.Vector2(-self.revThrust, 0)
                slewFuel += dt * self.revCost / 3 * 2
            elif self.slewR:
                slewVector = pygame.Vector2(self.revThrust, 0)
                slewFuel += dt * self.revCost / 3 * 2
            else:
                self.slewVector = pygame.Vector2(0, 0)

            # turning
            if rotateL and not thrustFwd:
                self.angularVelocity = -self.turnRate
                turnFuel = dt * self.turnCost
            elif rotateL and thrustFwd: # multiply steering by engine vec scalar
                thrustVectoredRate = self.turnRate * self.engVectoring
                self.angularVelocity = -thrustVectoredRate
                turnFuel = dt * self.turnCost
            elif rotateR and not thrustFwd:
                self.angularVelocity = self.turnRate
                turnFuel = dt * self.turnCost
            elif rotateR and thrustFwd: # multiply steering by engine vec scalar
                thrustVectoredRate = self.turnRate * self.engVectoring
                self.angularVelocity = thrustVectoredRate
                turnFuel = dt * self.turnCost
            else:
                self.angularVelocity = 0

        else:   # empty tank case
            self.fuel = 0

        # also seems like good candidates for segregating into src/engine/ module
        # or at least placing in unique functions; called single-line in update()
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

    # def getCargoMass
        # iterate contracts, collect positional loads (forward looking towards MOI)
        # iterate pax, random positional seating loads (...)
        # damaged cargo may affect mass? damage model in update? many questions
    
    # def MomentOfInertiaStuff
        # would only be useful if we abandon static turning and use conserved
        # angular momentum - loading screen would offer auto-load, or custom load
        # maybe more trouble than it is worth re: gameplay granularity/noticeableness