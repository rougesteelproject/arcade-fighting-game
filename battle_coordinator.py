from team import Team

class BattleCoordinator():
    def __init__(self, teams) -> None:
        self._teams = teams

        self._victor = None

    def _roll_initiative(self):
        for unit in self._units:
            unit.roll_initiative()

    def _check_living_units(self):
        living_units = [unit for unit in [team.living_members for team in self._teams]]
        return living_units

    def _get_targets(self, attacking_unit):
        targets = [unit for unit in [team.living_members for team in self._teams if team != attacking_unit.callback_team]]
        return targets

    def _check_victory(self):
        potential_winners = self._teams
        for team in self._teams:
            if not team.living_members:
                potential_winners.remove(team)
        if len(potential_winners) == 1:
            self._victor = potential_winners[0]
                



    def _do_round(self):
        self._roll_initiative()

        active_units = sorted(self._check_living_units(), key=lambda active_unit: active_unit.get_initiative_bar())
        for active_unit in active_units:
            if active_unit.is_alive and self._victor == None and active_unit.get_initiative_bar() >= self._initiative_threshold:
                target_list = self._get_targets(active_unit)
                damage, target = active_unit.do_game_tick(target_list, initiative_threshold)

                target.take_damage(damage)

                self._check_victory()

    def run_battle(self):
        
        for team in self._teams:
            team.combat_init()
            for unit in team.members:
                unit.combat_init()

        self._initiative_threshold = max([unit.get_max_initiative for unit in self._check_living_units])

        while self._victor == None:
            self._do_round()

        print(f'Team \"{self._victor.name}\" has won!')