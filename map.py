import os
import logging
import random
from enum import IntEnum

logger = logging.getLogger('Map')
logger.setLevel(logging.DEBUG)

class Tiles(IntEnum):
    PASSAGE = 0
    STONE = 1
    WALL = 2
    POWERUPS = 10
    BONUS = 11
    EXIT = 100


class Map:
    def __init__(self, level=1, enemies=0, size=(20, 20), mapa=None):
        self._level = level
        self._size = size
        self.hor_tiles = size[0]
        self.ver_tiles = size[1]
        self._walls = []
        self._enemies_spawn = [] 
    
        if not mapa:
            logger.info("Generating a MAP")
            self.map = [[Tiles.PASSAGE] * self.ver_tiles for i in range(self.hor_tiles)]
            while len(self._walls) < 2: #minimum of 2 walls
                for x in range(self.hor_tiles):
                    for y in range(self.ver_tiles):
                        if x in [0, self.hor_tiles-1] or y in [0, self.ver_tiles-1]:
                            self.map[x][y] = Tiles.STONE
                        else:
                            if random.randint(0,10) > 8:
                                self.map[x][y] = Tiles.WALL
                                self._walls.append((x, y))
                            elif x > self.hor_tiles/10 and y > self.ver_tiles/10 and random.randint(0,10) > 8 and len(self._enemies_spawn) < enemies:
                                self._enemies_spawn.append((x, y))
                    
            self.exit_door = random.choice(self._walls)
            self.powerup = random.choice([w for w in self._walls if w != self.exit_door]) #hide powerups behind walls only

        else:
            logger.info("Loading MAP")
            self.map = mapa
            for x in range(self.hor_tiles):
                for y in range(self.ver_tiles):
                    if self.map[x][y] == Tiles.WALL and (x, y) != (1,1):
                        self._walls.append((x, y))
        self._bomberman_spawn = (1,1) #Always true
    
    def __getstate__(self):
        return self.map
    
    def __setstate__(self, state):
        self.map = state        

    @property
    def size(self):
        return self._size

    @property
    def walls(self):
        return self._walls

    @property
    def level(self):
        return self._level

    @property
    def bomberman_spawn(self):
        return self._bomberman_spawn

    @property
    def enemies_spawn(self):
        return self._enemies_spawn

    def get_tile(self, pos):
        x, y = pos
        return self.map[x][y]

    def is_blocked(self, pos):
        x, y = pos
        if x not in range(self.hor_tiles) or y not in range(self.ver_tiles):
            return True
        if self.map[x][y] in [Tiles.STONE, Tiles.WALL]:
            return True
        return False

    def calc_pos(self, cur, direction):
        assert direction in "wasd" or direction == ""

        cx, cy = cur
        npos = cur
        if direction == 'w':
            npos = cx, cy-1
        if direction == 'a':
            npos = cx-1, cy
        if direction == 's':
            npos = cx, cy+1
        if direction == 'd':
            npos = cx+1, cy

        #test blocked
        if self.is_blocked(npos):
            return cur
   
        return npos
    
