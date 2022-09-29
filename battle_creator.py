import constants

from team import Team
from unit import Unit
import logging

class BattleCreator():
    def __init__(self, callback) -> None:
        
        self._game_loop = callback

        self._money_limit = constants.DEFAULT_MONEY_LIMIT

        self._teams = []   

    def dependant_init(self):
        self._game_version = constants.DEFAULT_GAME_VERSION
        self._reset_variance_and_initiative()

        while len(self._teams) < constants.MIN_NUMBER_OF_PLAYERS:
            self._add_team(f'team_{len(self._teams)+1}')

    def _set_game_version(self, new_game_version, sell_outdated_units):

            if sell_outdated_units:
                self._sell_outdated_units(new_game_version)

            self._recalculate_units(new_game_version)

            self._game_version = new_game_version

            self._reset_variance_and_initiative()

    def get_outdated_list(self, new_game_version):

        outdated_list = "The following units will be refunded: \n"

        for team in self._teams:
            team_outdated_list = team.list_outdated_members(new_game_version)

            if team_outdated_list != "":
                outdated_list += (f'''{team.name}:
                {team_outdated_list}
                --- \n''')

        return outdated_list

    def _sell_outdated_units(self, new_game_version):
        for team in self._teams:
            team.sell_outdated_units(self._game_version, new_game_version)

    def _recalculate_units(self, new_game_verison):
        for team in self._teams:
            team.change_game_version_recalculate_units(self._game_version, new_game_verison)

    def _reset_variance_and_initiative(self):
        if self._game_version == 1:
            self.use_initiative = False
            self.use_variance = False
        elif self._game_version >= 2:
            self.use_initiative = True
            if self._game_version >= 3:
                self.use_variance = True
            else:
                self.use_variance = False

        self._game_loop.battle_creator_disable_initiative(self.use_initiative)
        self._game_loop.battle_creator_disable_variance(self.use_variance)

    def buy_unit(self, unit, team_name):

            for team in self._teams:
                if team.name == team_name:
                    team_selection = team
                    break

            try:

                team_selection.buy(unit, self._game_version, self._money_limit)
            except:
                logging.exception("Failure to buy unit")

    def _sell_unit(self, team_to_sell_from_index, sell_unit_index):

        team_to_sell_from = self._teams[team_to_sell_from_index]

        team_to_sell_from.sell(team_to_sell_from.members[sell_unit_index], self._game_version)

    def _check_team_with_name_already_exists(self, team_name):
        for team in self._teams:
            if team.name == team_name:
                #TODO have a little pop up window for this
                print(f'A team exists already with the name {team_name}!')
                return True

        return False

    def _add_team(self, team_name):

        if not self._check_team_with_name_already_exists(team_name):
            self._teams.append(Team(team_name))
            self._game_loop.battle_creator_add_team_ui()

    def _remove_team(self, team_index):
        #TODO a popup to ask if you're really sure you want to delete a team with units in it
        if len(self._teams) > constants.MIN_NUMBER_OF_PLAYERS:
            del self._teams[team_index]

    def rename_team(self, new_name, team_index):
        other_teams = [team for index, team in enumerate(self._teams) if index != team_index]

        name_available = True

        for team in other_teams:
            if team.name == new_name:
                name_available = False
                break

        if name_available:
            self._teams[team_index].name = new_name

    def _set_money_limit(self, money_limit):
        self._money_limit = int(money_limit)

    def _check_all_teams_have_members(self):
        all_teams_have_members = True
        for team in self._teams:
            if len(team.members) == 0:
                all_teams_have_members = False
                #TODO make this a popup
                print(f'Team {team.name} does not have any members!')

        return all_teams_have_members

    def _check_all_teams_in_budget(self):
        all_teams_in_budget = True
        for team in self._teams:
            if team.cost > self._money_limit:
                all_teams_in_budget = False
                #TODO make ths a popup
                print(f'Team {team.name} not under budget!')
                break

        return all_teams_in_budget

    def _run_battle(self):
        if self._check_all_teams_have_members():
            if self._check_all_teams_in_budget():
                self._game_loop.run_battle()

    def _exit(self):
        pass