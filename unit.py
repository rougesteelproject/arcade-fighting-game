import math
from random import randint, uniform
from shutil import register_unpack_format
import constants

class Unit:
    def __init__(self, name: str, base_health: int, min_attack: int, max_attack: int, min_initiative: float, max_initiative: float, ai_type: str, price:int = 0, team:str = None, game_version:float = 3) -> None:
        self.is_invalid = False

        self.name = name

        self._base_health = base_health
        self._min_attack = min_attack
        self._max_attack = max_attack
        self._min_initiative = min_initiative
        self._max_initiative = max_initiative

        self._team = team
        self._ai = self._set_ai(ai_type)

        self._game_version = game_version

        self._price = price

        self._check_validity()

        if not self.is_invalid:
            self._price = self._set_price()

        else: 
            self._price = None

        self.id = 0

    def _check_validity(self):
        if self._base_health < 1:
            print("Base health must be at least 1!") 
            self.is_invalid = True
        
        if self._min_attack < 0:
            print("Min attack cannot be negative!")
            self.is_invalid = True

        if self._max_attack < self._min_attack:
            print("Max attack must be greater than min attack!")
            self.is_invalid = True

        if (self._max_initiative < self._min_initiative):
            print("Max initiative must be greater than min!")
            self.is_invalid = True

        if self._min_initiative <= 0:
            print("min initiative must be greater than zero!")
            self.is_invalid = True

    def _set_ai(self, ai_type):
        if ai_type == 'basic':
            from ais.basic_ai import BasicAI
            return BasicAI(self)
        
    def get_max_initiative(self):
        return self._max_initiative

    def _set_attack_value(self):
        self._attack_value = (self._min_attack + self._max_attack)/2

    def _set_initiative_value(self):
        self._initiative_value = ((math.sqrt(self._max_initiative/self._min_initiative))*self._min_initiative)**1.1

    def _set_price(self):
        self._set_attack_value()

        self._set_initiative_value()

        self._offensive_power = self._attack_value * self._initiative_value *5

        price = (2*(self._base_health + self._offensive_power) + 3*(math.sqrt(self._base_health * self._offensive_power) *2))/5
        
        return price

    def get_price(self):
        if self._price == None:
            print("Tried to get price from a unit with invalid stats.")
        return self._price

    def set_callback_team(self, callback_team):
        self.callback_team = callback_team

    def combat_init(self):
        self._current_health = self._base_health
        self._initiative_bar = 0
        self.is_alive = True

    def get_initiative_bar(self):
        return self._initiative_bar

    def attack_roll(self):
        return randint(self._mix_attack, self._max_attack)

    def _check_is_alive(self):
        if self._current_health <= 0:
            self.is_alive = False

    def take_damage(self, damage):
        self._current_health -= damage

        self._check_is_alive()
        
        if not self.is_alive:
            self._callback_team.kill_unit(self)

    def roll_initiative(self):
        n = constants.INITIATIVE_NUMBER_OF_POSIBILITIES
        x = uniform(0,n)
        roll = self._min_init * [self._max_init/self._min_init]**(x/n)
        self._initiative_bar += roll

    def set_id(self, id):
        self.id = id

    def do_game_tick(self, targets, initiative_threshold):
        damage, target = self._ai.do_game_tick(targets)

        self._initiative_bar -= initiative_threshold

        return damage, target