import math

class Unit:
    def __init__(self, base_health: int, min_attack: int, max_attack: int, min_initiative, max_initiative, team, ai_type) -> None:
        self.is_invalid = False
        
        self._base_health = base_health
        self._min_attack = min_attack
        self._max_attack = max_attack
        self._min_initiative = min_initiative
        self._max_initiative = max_initiative

        self._team = team
        self._ai_type = ai_type

        self._check_validity()

        if not self.is_invalid:

            self._set_attack_value()

            self._set_initiative_value()

            self._offensive_power = self._attack_value * self._initiative_value *5

            self._price = self._set_price()

        else: 
            self._price = None

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
        
    def _set_attack_value(self):
        self._attack_value = (self._min_attack + self._max_attack)/2

    def _set_initiative_value(self):
        self._initiative_value = ((math.sqrt(self._max_initiative/self._min_initiative))*self.min_initiative)^1.1

    def _set_price(self):
        price = 0

        price = (2*(self._base_health + self._offensive_power) + 3*(math.sqrt(self._base_health * self._offensive_power) *2))/5
        
        return price

    def get_price(self):
        if not self.is_invalid:
            return self._price
        
        else:
            print("Tried to get price from a unit with invalid stats.")
            return None
            