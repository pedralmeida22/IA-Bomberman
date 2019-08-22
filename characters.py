
DEFAULT_LIVES = 3

class Character:
    def __init__(self, x=1, y=1):
        self._pos = x, y
    
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

class Bomberman(Character):
    def __init__(self, pos, lives=DEFAULT_LIVES):
        super().__init__(x=pos[0], y=pos[1])
        self._spawn_pos = pos
        self._lives = lives
        self._powers = []
    
    def to_dict(self):
        return {"pos": self.pos,
                "lives": self._lives}

    @property 
    def powers(self):
        return self._powers

    @property
    def lives(self):
        return self._lives

    def respawn(self):
        self.pos = self._spawn_pos

    def kill(self):
        self._lives-=1

    def powerup(self, _type):
        self._powers.append(_type)

class Enemy(Character):
    def __init__(self, name, points, speed, smart, wallpass):
        self._name = name
        self._points = points
        self._speed = speed
        self._smart = smart
        self._wallpass = wallpass
    
    def __str__(self):
        return f"{self._name}"
    
    @property
    def points(self):
        self._points
    
class Balloom(Enemy):
    def __init__(self):
        super().__init__(self.__class__.__name__,
            100, 2, 1, False)

class Oneal(Enemy):
    def __init__(self):
        super().__init__(self.__class__.__name__,
            200, 3, 2, False)

  