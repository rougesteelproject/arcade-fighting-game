import arcade

from ais.basic_ai import BasicAI

import constants

class BattleCoordinator(arcade.View):
    def __init__(self, window: arcade.Window, teams, use_initiative, use_variance, game_loop) -> None:
        super().__init__(window)
        self._teams = teams

        self._victor = None

        self.bar_list = arcade.SpriteList()

        self._game_loop = game_loop

        self._use_initiative = use_initiative
        self._use_variance = use_variance

    def setup(self):
        self.background = arcade.load_texture("./arcade_view_classes/backgrounds/map_13x13.png")

        self._setup_teams() 

        self._end_of_round = True
        self._tick_index = 0

        self._show_floating_damage = False

        self._game_tick_timer = 0

        self._check_victory()  

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background)

        for team in self._teams:
            team.draw()

        if self._show_floating_damage:
            self._floating_damage_text.draw()

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.GRAY)

    def _roll_initiative(self):
        for unit in self._living_units:
            unit.roll_initiative(self._use_variance, self._initiative_threshold)

    def _get_living_units(self):
        self._living_units = arcade.SpriteList()

        for team in self._teams:
            self._living_units.extend(team.sprite_list)

    def _get_targets(self, attacking_unit):
        targets = [unit for unit in self._living_units if unit.callback_team != attacking_unit.callback_team]
        return targets

    def _check_victory(self):
        potential_winners = self._teams
        for team in self._teams:
            if not team.sprite_list:
                potential_winners.remove(team)
        if len(potential_winners) == 0:
            print("It\'s a draw!")
            self._victor = None
            self._declare_victor()
        elif len(potential_winners) == 1:
            self._victor = potential_winners[0]
            print(f'Team \"{self._victor.name}\" has won!')
            self._declare_victor()

    def _do_ai_tick(self, unit, game_data):
        #TODO battle_coordinator imports and uses BattleData() or something
        
        #TODO there's gotta be a better way to do this. Maybe battle_coordinator has a list of AI?

        for ai_type in unit._ai_types:
            if ai_type == "basic":
                if not hasattr(self, '_basic_ai'):
                    self._basic_ai = BasicAI()
                return self._basic_ai.do_game_tick(unit, game_data['targets'], self._use_variance)
                #TODO change to getting all enemies of a given unit

    def _start_new_round(self):
        self._end_of_round = False

        if self._use_initiative:    
            self._set_initiative_threshold()

        if self._use_initiative:
            self._roll_initiative()

            self.active_units = sorted(self._living_units, key=lambda active_unit: active_unit.get_current_initiative(), reverse=True)
        else:
            self.active_units = self._living_units()
            self._initiative_threshold = 0

    def on_update(self, delta_time: float):

        for team in self._teams:
            team.on_update(delta_time)
        
        self._game_tick_timer += delta_time

        if self._game_tick_timer > constants.DELTA_TIME:
            self._game_tick_timer = 0.0
            self._do_game_tick()

    def _do_game_tick(self):

        self._show_floating_damage = False

        if self._end_of_round:
            self._start_new_round()
            self._tick_index = 0
        else:
            self._tick_index += 1
        
        active_unit = self.active_units[self._tick_index]
            

        #Units remove themselves from spritelists as they die
        if self._use_initiative and active_unit.get_current_initiative() >= self._initiative_threshold:
            unit_can_attack = True
        elif self._use_initiative == False:
            unit_can_attack = True
        else:
            unit_can_attack = False

        if unit_can_attack and self._victor == None: 
            game_data = {'targets' : self._get_targets(active_unit)}
            damage, target = self._do_ai_tick(active_unit, game_data)
            
            if self._use_initiative:
                active_unit.expend_initiative(self._initiative_threshold)

            print(f'{active_unit._name} on team {active_unit.callback_team.name} {active_unit._attack_verb} {target._name} on team {target.callback_team.name} for {damage} damage!')
            
            active_unit.attack_animation(target)

            self.floating_damage(target, damage)

            target.take_damage(damage)

        if active_unit == self.active_units[-1]:
            self._end_of_round = True

        self._check_victory()

    def _setup_teams(self):
        if len(self._teams) == 2:
            #TODO account for the other sides of the hexagon
            self._teams[0].setup(constants.ARENA_SLOT_2)
            self._teams[1].setup(constants.ARENA_SLOT_1)

        for team in self._teams:
            for index, unit in enumerate(team):
                #Smallest multiple of 5 less than the index
                row = (index // 5) * 5
                unit.setup(index, team._arena_slot, row, self.bar_list)
        self._get_living_units()

    def _set_initiative_threshold(self):
        self._initiative_threshold = max([unit.get_max_initiative() for unit in self._living_units])

    def floating_damage(self, target, damage):
        self._floating_damage_text = arcade.Text(text=str(damage), start_x=target.center_x, start_y=target.center_y)
        self._show_floating_damage = True

    def _declare_victor(self):
        self._game_loop.declare_victor(self._victor)
