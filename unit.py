import arcade

from typing import Tuple
import logging
import math
from random import randint, uniform

import constants

#TODO add fields for "Modpack" and "Creator_Email"

class Unit(arcade.Sprite):
    def __init__(self, name: str, base_health: int, min_attack: int, ai_types: list = ['basic'], game_version:float = 3, attack_verb:str = "attacked", filename:str = None) -> None:

        super().__init__(filename=filename)

        self._name = name

        self._game_version = int(game_version)

        self._base_health = int(base_health)
        
        self._min_attack = int(min_attack)
        self._max_attack = self._min_attack
        

        self._attack_verb = attack_verb

        self._ai_types = ai_types

    @staticmethod
    def from_dict(source):

        unit = Unit(name = source[u'_name'], base_health = source[u'_base_health'],  min_attack = source[u'_min_attack'], ai_types= source[u'_ai_types'], game_version= source[u'_game_version'], attack_verb= source['_attack_verb'], filename=source['filename'])
        
        if u'_max_attack' in source:
            unit._max_attack = int(source[u'_max_attack'])

        if u'_min_initiative' in source:
            unit._min_initiative = float(source[u'_min_initiative'])
            if u'_max_initiative' in source:
                unit._max_initiative = float(source[u'_max_initiative'])
            else:
                unit._max_initiative = unit._min_initiative

        if u'_raw_power_v3' in source:
            unit.raw_power_v3 = int(source[u'_raw_power_v3'])
        
            
        if u'_raw_power_v2' in source:
            unit.raw_power_v2 = int(source[u'_raw_power_v2'])
        
        if u'_raw_power_v1' in source:
            unit.raw_power_v1 = int(source[u'_raw_power_v1'])
            

        return unit

    def to_dict(self):
        return self.__dict__

    def setup(self, index, arena_slot, row, bar_list):
        self._current_health = self._base_health
        self._current_initiative = 0
        self._is_alive = True
        self._get_initial_position(index, arena_slot, row)
        self.health_indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
        )
        self.initiative_indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
        )

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
        self._raw_power_v1 = self._round_one_minimum(raw_power_v1)

    def _set_raw_power_v2(self):
        raw_power_v2 = (2 * (self._base_health + (5 * self._min_attack * (self._max_initiative ** 1.1))) + 3 * ( ( math.sqrt(self._base_health* 5 * self._min_attack) ) * 2) ) / 5
        self._raw_power_v2 = self._round_one_minimum(raw_power_v2)

    def _set_raw_power_v3(self):
        self._set_attack_value()
        self._set_initiative_value()

        self._offensive_power = self._attack_value * self._initiative_value *5

        raw_power_v3 = (2*(self._base_health + self._offensive_power) + 3*(math.sqrt(self._base_health * self._offensive_power) *2))/5
        self._raw_power_v3 = self._round_one_minimum(raw_power_v3)

    def _set_raw_powers(self):
        #TODO move this to the db_cont
        
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

        if self._game_version >= game_version and not hasattr(self, f'_raw_power_v{game_version}'):
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
        #TODO can I get the parent spritelist?

    def _get_initial_position(self, index, arena_slot, row):
        #Row starts at zero
        self.center_x = arena_slot['first_unit_center']['x'] + (arena_slot['unit_spacing']['x'] * index) + (arena_slot['row_spacing']['x'] * (row))
        self.center_y = arena_slot['first_unit_center']['y'] + (arena_slot['unit_spacing']['y'] * index) + (arena_slot['row_spacing']['y'] * (row ))

    def get_current_initiative(self):
        return self._current_initiative

    def attack_roll(self, use_variance):
        if use_variance:
            return randint(self._min_attack, self._max_attack)
        else:
            return self._max_attack

    def _check_is_dead(self):
        if self._current_health <= 0:
            self._is_alive = False

            print(f'{self._name} on team {self.callback_team.name} has died.')

            self.kill()

    def take_damage(self, damage):
        self._current_health -= damage

        # Set the player's indicator bar fullness
        self.health_indicator_bar.fullness = (
            self._current_health / self._base_health
        )

        self._check_is_dead()

    def roll_initiative(self, use_variance, initiative_threshold):
        if use_variance:
            n = constants.INITIATIVE_NUMBER_OF_POSIBILITIES
            x = uniform(0,n)
            roll = self._min_initiative * (self._max_initiative/self._min_initiative)**(x/n)
        else:
            roll = self._max_initiative
        self._current_initiative += roll

        # Set the player's indicator bar fullness
        self.initiative_indicator_bar.fullness = (
            self._current_initiative / initiative_threshold
        )

    def expend_initiative(self, initiative_threshold):
        self._current_initiative -= initiative_threshold

        # Set the player's indicator bar fullness
        self.initiative_indicator_bar.fullness = (
            self._current_initiative / initiative_threshold
        )

    def do_game_tick(self, targets, use_variance):
        damage, target = self._ai.do_game_tick(targets, use_variance)
            
        return damage, target

#This has to be here to prevent circular imports
class IndicatorBar:
    """
    Represents a bar which can display information about a sprite.

    :param Player owner: The owner of this indicator bar.
    :param arcade.SpriteList sprite_list: The sprite list used to draw the indicator
    bar components.
    :param Tuple[float, float] position: The initial position of the bar.
    :param arcade.Color full_color: The color of the bar.
    :param arcade.Color background_color: The background color of the bar.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
        self,
        owner: Unit,
        sprite_list: arcade.SpriteList,
        position: Tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 100,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: Unit = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.position: Tuple[float, float] = position

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)