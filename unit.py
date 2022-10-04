import logging
import math
from random import randint, uniform
import constants

#TODO add fields for "Modpack" and "Creator_Email"

class Unit:
    def __init__(self, name: str, base_health: int, min_attack: int, ai_types: list = ['basic'], game_version:float = 3, attack_verb:str = "attacked") -> None:

        self._name = name

        self._game_version = int(game_version)

        self._base_health = int(base_health)
        
        self._min_attack = int(min_attack)
        self._max_attack = self._min_attack
        

        self._attack_verb = attack_verb

        self._ai_types = ai_types

    @staticmethod
    def from_dict(source):

        unit = Unit(name = source[u'_name'], base_health = source[u'_base_health'],  min_attack = source[u'_min_attack'], ai_types= source[u'_ai_types'], game_version= source[u'_game_version'], attack_verb= source['_attack_verb'])
        
        if u'_max_attack' in source:
            unit._max_attack = source[u'_max_attack']

        if u'_min_initiative' in source:
            unit._min_initiative = source[u'_min_initiative']
            if u'_max_initiative' in source:
                unit._max_initiative = source[u'_max_initiative']
            else:
                unit._max_initiative = unit._min_initiative

        if u'_raw_power_v3' in source:
            unit.raw_power_v3 = source[u'_raw_power_v3']
        
            
        if u'_raw_power_v2' in source:
            unit.raw_power_v2 = source[u'_raw_power_v2']
        
        if u'_raw_power_v1' in source:
            unit.raw_power_v1 = source[u'_raw_power_v1']
            

        return unit

    def to_dict(self):
        return self.__dict__

    def _check_stat_validity(self):
        #note to self, keep this consistent with unit_creator
        self._is_invalid_v1 = False
        self._is_invalid_v2 = False
        self._is_invalid_v3 = False

        if self._base_health < 1:
            print("Base health must be at least 1!") 
            self._is_invalid_v1 = True
            self._is_invalid_v2 = True
            self._is_invalid_v3 = True
        
        if self._min_attack < 0:
            print("Min attack cannot be negative!")
            self._is_invalid_v1 = True
            self._is_invalid_v2 = True
            self._is_invalid_v3 = True

        if self._game_version >= 3  and self._max_attack < self._min_attack:
            print("Max attack must be greater than or equal to min attack!")

            self._is_invalid_v3 = True

        if self._game_version >= 3 and (self._max_initiative < self._min_initiative):
            print("Max initiative must be greater than or equal to min!")

            self._is_invalid_v3 = True
        
        if self._game_version >= 2 and self._min_initiative < 0:
            print("min initiative cannot be negative. It must be at least zero!")
            self._is_invalid_v2 = True

        if self._game_version >= 3 and self._min_initiative == 0:
            print("min initiative must be greater than zero!")
            self._is_invalid_v3 = True

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

    def _round_one_minimum(self, base_raw_power):

        if round(base_raw_power) <= 0:
            rounded_raw_power = 1
        else:
            rounded_raw_power = round(base_raw_power) #rounding to the nearest integer

        return rounded_raw_power

    def _set_raw_power_v1(self):
        raw_power_v1  = (2 * (self._base_health + (5 * self._min_attack)) + 3 * ( ( math.sqrt(self._base_health* 5 * self._min_attack) ) * 2) ) / 5
        self.raw_power_v1 = self._round_one_minimum(raw_power_v1)

    def _set_raw_power_v2(self):
        raw_power_v2 = (2 * (self._base_health + (5 * self._min_attack * (self._max_initiative ** 1.1))) + 3 * ( ( math.sqrt(self._base_health* 5 * self._min_attack) ) * 2) ) / 5
        self.raw_power_v2 = self._round_one_minimum(raw_power_v2)

    def _set_raw_power_v3(self):
        self._set_attack_value()
        self._set_initiative_value()

        self._offensive_power = self._attack_value * self._initiative_value *5

        raw_power_v3 = (2*(self._base_health + self._offensive_power) + 3*(math.sqrt(self._base_health * self._offensive_power) *2))/5
        self.raw_power_v3 = self._round_one_minimum(raw_power_v3)

    def _set_raw_powers(self):
        
        self._check_stat_validity()
        #this is for when a unit is created by db_cont

        if self._game_version >= 3:
            if self._is_invalid_v3 == False:
                self._set_raw_power_v3()
            else:
                self.raw_power_v3 = None

        if self._game_version >= 2:
            if self._is_invalid_v2 == False:
                self._set_raw_power_v2()
            else:
                self.raw_power_v2 = None

        if self._game_version >= 1:
            if self._is_invalid_v1 == False:
                self._set_raw_power_v1()
            else:
                self.raw_power_v1 = None

    def get_raw_power(self, game_version):

        if self._game_version >= game_version and not hasattr(self, f'raw_power_v{game_version}'):
            self._set_raw_powers()

        if game_version == 3:
            raw_power = self._raw_power_v3
        elif game_version == 2:
            raw_power = self._raw_power_v2
        elif game_version == 1:
            raw_power = self._raw_power_v1

        if raw_power == None:
            logging.error("Tried to get raw_power from a unit with invalid stats.")
        return raw_power

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

    def expend_initiative(self, initiative_threshold):
        self._initiative_bar -= initiative_threshold

    def do_game_tick(self, targets, use_variance):
        damage, target = self._ai.do_game_tick(targets, use_variance)
            
        return damage, target

    def get_is_alive(self):
        return self._is_alive