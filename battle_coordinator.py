import arcade

from ais.basic_ai import BasicAI

class BattleCoordinator(arcade.View):
    def __init__(self, window: arcade.Window, teams, use_initiative, use_variance) -> None:
        super().__init__(window)
        self._teams = teams

        self._victor = None

        self._use_initiative = use_initiative
        self._use_variance = use_variance

    def setup(self):
        self.background = arcade.load_texture("/backgrounds/map_13x13.png")

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        for team in self._teams:
            team.draw()

    #TODO change delta time
    #TODO do I need this?
    def on_update(self, delta_time: float):
        self._do_game_tick()
        return super().on_update(delta_time)

    def _roll_initiative(self):
        for unit in self._check_living_units():
            unit.roll_initiative(self._use_variance)

    def _check_living_units(self):
        living_units = []
        for team in self._teams:
            living_units += team.get_living_members()
        return living_units

    def _get_targets(self, attacking_unit):
        living = self._check_living_units()
        targets = [unit for unit in living if unit.callback_team != attacking_unit.callback_team]
        return targets

    def _check_victory(self):
        potential_winners = self._teams
        for team in self._teams:
            if not team.get_living_members():
                potential_winners.remove(team)
        if len(potential_winners) == 0:
            print("It\'s a draw!")
            self._victor = "Nobody!"
        elif len(potential_winners) == 1:
            self._victor = potential_winners[0]
            print(f'Team \"{self._victor.name}\" has won!')

    def _do_game_tick(self, unit, game_data):
        #TODO battle_coordinator imports and uses BattleData() or something
        
        #TODO there's gotta be a better way to do this. Maybe battle_coordinator has a list of AI?

        for ai_type in unit._ai_types:
            if ai_type == "basic":
                if not hasattr(self, '_basic_ai'):
                    self._basic_ai = BasicAI()
                return self._basic_ai.do_game_tick(unit, game_data['targets'], self._use_variance)
                #TODO change to getting all enemies of a given unit

    def _do_round(self):
        
        if self._use_initiative:
            self._roll_initiative()

            active_units = sorted(self._check_living_units(), key=lambda active_unit: active_unit.get_initiative_bar(), reverse=True)
        else:
            active_units = self._check_living_units()
            self._initiative_threshold = 0

        for active_unit in active_units:
            if self._use_initiative and active_unit.get_initiative_bar() >= self._initiative_threshold:
                unit_can_attack = active_unit.get_is_alive()
            else:
                unit_can_attack = True

            if unit_can_attack and self._victor == None: 
                game_data = {'targets' : self._get_targets(active_unit)}
                damage, target = self._do_game_tick(active_unit, game_data)
                
                if self._use_initiative:
                    active_unit.expend_initiative(self._initiative_threshold)

                print(f'{active_unit._name} on team {active_unit.callback_team.name} {active_unit._attack_verb} {target._name} on team {target.callback_team.name} for {damage} damage!')
                
                target.take_damage(damage)

                if self._use_initiative:
                    target.check_is_dead()

                    self._check_victory()

        if self._use_initiative == False:
            for active_unit in active_units:
                active_unit.check_is_dead()

            self._check_victory()

    def _initialize_teams(self):
        for team in self._teams:
            team.combat_init()
            for unit in team.members:
                unit.combat_init()

    def _set_initiative_threshold(self):
        unit_list = self._check_living_units()
        self._initiative_threshold = max([unit.get_max_initiative() for unit in unit_list])

    def run_battle(self):
        
        self._initialize_teams()        

        if self._use_initiative:    
            self._set_initiative_threshold()

        self._check_victory()

        while self._victor == None:
            self._do_round()