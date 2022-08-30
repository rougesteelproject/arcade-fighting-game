import math
from random import randint, uniform
import constants

class Unit:
    def __init__(self, name: str, base_health: int, min_attack: int, max_attack: int, min_initiative: float, max_initiative: float, ai_type: str, price_v1:int = None, price_v2:int = None, price_v3:int = None, game_version:float = 3, attack_verb:str = "attacked") -> None:

        self.name = name

        self._base_health = base_health
        
        self._min_attack = min_attack
        
        if game_version >= 3: # variable attack was added in v3
            self._max_attack = max_attack
        else:
            self._max_attack = min_attack

        if game_version >= 2: #initiative added in v2
            self._min_initiative = min_initiative
        
        if game_version >= 3: #variable initiative added in v3
            self._max_initiative = max_initiative
        else:
            self._max_initiative = min_initiative

        self.attack_verb = attack_verb

        self._ai = self._set_ai(ai_type)

        self._game_version = game_version

        if price_v1 == None and self._game_version == 1:
            self._set_prices()
        elif price_v2 == None and self._game_version == 2:
            self._set_prices()
        elif price_v3 == None and self._game_version == 3:
            self._set_prices()
        else:
            self.price_v1 = price_v1
            self.price_v2 = price_v2
            self.price_v3 = price_v3

        self.id = 0

    def _check_stat_validity(self):
        #note to self, keep this consistent with unit_creator
        self.is_invalid_v1 = False
        self.is_invalid_v2 = False
        self.is_invalid_v3 = False

        if self._base_health < 1:
            print("Base health must be at least 1!") 
            self.is_invalid_v1 = True
            self.is_invalid_v2 = True
            self.is_invalid_v3 = True
        
        if self._min_attack < 0:
            print("Min attack cannot be negative!")
            self.is_invalid_v1 = True
            self.is_invalid_v2 = True
            self.is_invalid_v3 = True

        if self._game_version >= 2  and self._max_attack < self._min_attack:
            print("Max attack must be greater than or equal to min attack!")
            self.is_invalid_v2 = True
            self.is_invalid_v3 = True

        if self._game_version >= 2 and (self._max_initiative < self._min_initiative):
            print("Max initiative must be greater than or equal to min!")
            self.is_invalid_v2 = True
            self.is_invalid_v3 = True
        
        if self._game_version >= 2 and self._min_initiative < 0:
            print("min initiative cannot be negative. It must be at least zero!")
            self.is_invalid_v2 = True
            self.is_invalid_v3 = True
        elif self._game_version >= 3 and self._min_initiative == 0:
            print("min initiative must be greater than zero!")
            self.is_invalid_v3 = True


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

    def _round_one_minimum(base_price):

        if round(base_price) <= 0:
            rounded_price = 1
        else:
            rounded_price = round(base_price) #rounding to the nearest integer

        return rounded_price

    def _set_price_v1(self):
        price_v1  = (2 * (self._base_health + (5 * self._min_attack)) + 3 * ( ( math.sqrt(self._base_health* 5 * self._min_attack) ) * 2) ) / 5
        self.price_v1 = self.round_one_minimum(price_v1)

    def _set_price_v2(self):
        price_v2 = (2 * (self._base_health + (5 * self._min_attack * (self._max_initiative ** 1.1))) + 3 * ( ( math.sqrt(self._base_health* 5 * self._min_attack) ) * 2) ) / 5
        self.price_v2 = self._round_one_minimum(price_v2)


    def _set_price_v3(self):
        self._set_attack_value()
        self._set_initiative_value()

        self._offensive_power = self._attack_value * self._initiative_value *5

        price_v3 = (2*(self._base_health + self._offensive_power) + 3*(math.sqrt(self._base_health * self._offensive_power) *2))/5
        self.price_v3 = self._round_one_minimum(price_v3)


    def _set_prices(self):
        
        self._check_stat_validity()

        if not self._is_invalid_v3:
            self._set_price_v3()
        else:
            self.price_v3 = None

        if not self._is_invalid_v2:
            self._set_price_v2()
        else:
            self.price_v2 = None

        if not self._is_invalid_v1:
            self._set_price_v1()
        else:
            self.price_v1 = None


    def get_price(self, game_version):

        if game_version == 3:
            price = self.price_v3
        elif game_version == 2:
            price = self.price_v2
        elif game_version == 1:
            price = self.price_v1

        if price == None:
            print("Tried to get price from a unit with invalid stats.")
        return price

    def set_callback_team(self, callback_team):
        self.callback_team = callback_team

    def combat_init(self):
        self._current_health = self._base_health
        self._initiative_bar = 0
        self._is_alive = True

    def get_initiative_bar(self):
        return self._initiative_bar

    def attack_roll(self, use_variance):
        if use_variance:
            return randint(self._min_attack, self._max_attack)
        else:
            return self._max_attack

    def check_is_dead(self):
        if self._current_health <= 0:
            self._is_alive = False

            print(f'{self.name} on team {self.callback_team.name} has died.')
            self.callback_team.kill_unit(self)

    def take_damage(self, damage):
        self._current_health -= damage

    def roll_initiative(self, use_variance):
        if use_variance:
            n = constants.INITIATIVE_NUMBER_OF_POSIBILITIES
            x = uniform(0,n)
            roll = self._min_initiative * (self._max_initiative/self._min_initiative)**(x/n)
        else:
            roll = self._max_initiative
        self._initiative_bar += roll

    def set_id(self, id):
        self.id = id

    def expend_initiative(self, initiative_threshold):
        self._initiative_bar -= initiative_threshold

    def do_game_tick(self, targets, use_variance):
        damage, target = self._ai.do_game_tick(targets, use_variance)
            
        return damage, target

    def get_is_alive(self):
        return self._is_alive