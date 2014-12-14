__author__ = 'sasau'

BAT_AT_RIGHT = 0
BAT_AT_LEFT = 1
BAT_AT_SWITCH = 2

THROW_AT_RIGHT = 0
THROW_AT_LEFT = 1


class PitcherAbility(object):
    def __init__(self):
        super().__init__()
        self.speed = 80
        self.stamina = 0
        self.control = 0
        self.has_breaking_ball = {}
        self.special_ability = ()


class FielderAbility(object):
    def __init__(self):
        super().__init__()
        self.ballistic = 1
        self.bat_control = 0
        self.power = 0
        self.speed = 1
        self.shoulder = 1
        self.fielding = 1
        self.error = 1
        self.special_ability = ()


class Player(object):
    def __init__(self):
        super().__init__()
        self.name = None
        self.bat_at = None
        self.throw_at = None
        self.position = None
        self.sub_position = ()
        self.fielder_ability = FielderAbility()
        self.pitcher_ability = PitcherAbility()
