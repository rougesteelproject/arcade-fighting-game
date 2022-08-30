from constants import LIMIT_NUMBER_OF_PLAYERS
from menu import Menu
from team import Team
from unit import Unit
import traceback

class BattleCreator():
    def __init__(self, callback, money_limit, game_version) -> None:
        
        self._callback = callback

        self._database_controller = self._callback._database_controler

        self._game_version = game_version
        self._enable_other_version_units = False

        self._money_limit = money_limit

        self._search_bar_units_data = []

        self._teams = []

        while len(self._teams) < 2:
            self._add_team()

        self._set_use_initiative()
        self._set_use_variability()

    def _set_use_initiative(self):
        if self._game_version >= 2:
            self._use_initiative = True
        else:
            self._use_initiative = False

    def _set_use_variability(self):
        if self._game_version >= 3:
            self._use_variability = True
        else:
            self._use_variability = False

    def _search_and_buy_units_by_name(self, name):
        self._search_bar_units_data = self._database_controller.get_unit_list_by_name(unit_name=name, game_version=self._game_version, enable_other_version_units=self._enable_other_version_units)

        unit_prompt = ""
        
        if len(self._search_bar_units_data) != 0:
            for index, unit_data in enumerate(self._search_bar_units_data):
                unit_prompt += f'{index}: {unit_data["name"]}: {unit_data["price"]} \n'

            unit_menu = Menu("Search Results:", unit_prompt, number_of_options=len(self._search_bar_units_data))

            unit_data = self._search_bar_units_data[unit_menu.get_selection()]
            

            team_prompt = ""

            for index, team in enumerate(self._teams):
                team_prompt += f'{index}: {team.name} \n'

            team_menu = Menu("Add to which team?", team_prompt, len(self._teams))

            team_selection = self._teams[team_menu.get_selection()]

            try:
                unit_selection = Unit(name=unit_data['name'], base_health=unit_data['base_health'], min_attack=unit_data['min_attack'], max_attack=unit_data['max_attack'], min_initiative=unit_data['min_initiative'], max_initiative=unit_data['max_initiative'], ai_type=unit_data['ai_type'], price=unit_data['price'], game_version=unit_data['game_version'], attack_verb=unit_data['attack_verb'])
                unit_selection._check_stat_validity()

                if self._game_version == 1 and unit_selection.is_invalid_v1 == False:
                    team_selection.buy(unit_selection)
                elif self._game_version == 2 and unit_selection.is_invalid_v2 == False:
                    team_selection.buy(unit_selection)
                elif self._game_version == 3 and unit_selection.is_invalid_v3 == False:
                    team_selection.buy(unit_selection)
            except:
                traceback.print_exc()

    def _sell_unit(self):
        sell_team_prompt = """Select team to sell from: \n"""

        for index, team in enumerate(self._teams):
            sell_team_prompt += f'{index}: {team.name} \n'


        sell_team_menu = Menu("Sell: ", sell_team_prompt, len(self._teams))

        team_to_sell_from = self._teams[sell_team_menu.get_selection()]

        sell_unit_prompt = """"""

        for index, unit in enumerate(team_to_sell_from.members):
            sell_unit_prompt += f'{index}: {unit.name}: {unit.get_price()} \n'

        sell_unit_menu = Menu("Which unit?", sell_unit_prompt, len(team_to_sell_from.members) + 1)

        team_to_sell_from.sell(team_to_sell_from.members[sell_unit_menu.get_selection()])

    def _check_team_with_name_already_exists(self, team_name):
        for team in self._teams:
            if team.name == team_name:
                print(f'A team exists already with the name {team_name}!')
                return True

        return False

    def _add_team(self):
        print("Adding team: \n")
        team_name = input("Team name: ")
        if not self._check_team_with_name_already_exists(team_name):
            self._teams.append(Team(team_name, self._money_limit))

    def _show_teams(self):
        for team in self._teams:
            print('---')
            print(f'{team.name}:')
            print(f'Money: {team.money}')
            print(team.list_members_grouped())

    def _check_all_teams_have_members(self):
        all_teams_have_members = True
        for team in self._teams:
            if not team.members:
                all_teams_have_members = False
                print(f'Team {team.name} does not have any members!')

        return all_teams_have_members


    def _run_battle(self):
        self._callback.run_battle(self._teams, self._use_initiative)

    def loop(self):

        loop = True

        while loop:

            prompt = """
            0: Add team
            1: Search for a unit to add
            2: Sell a unit:
            3: See Teams:
            4: Play the Battle!
            5: Exit to Main Menu
            6: Enable Units From Other Versions of the Game
            """

            menu = Menu("Battle Creator", prompt, number_of_options=7)

            selection = menu.get_selection()

            if selection == 0:
                self._add_team()
                self._show_teams

            elif selection == 1:
                name = input("Unit Name (Search): ")
                self._search_and_buy_units_by_name(name)
                self._show_teams()

            elif selection == 2:
                self._sell_unit()
                self._show_teams()

            elif selection == 3:
                self._show_teams()

            elif selection == 4:
                if self._check_all_teams_have_members():
                    self._run_battle()
                    loop = False

            elif selection == 5:
                loop = False

            elif selection == 6:
                if self._game_version >= 2:
                    print("Do you want to enable older/younger units? These may not work properly.")
                    enable_other_input = ""
                    while enable_other_input != "y" and enable_other_input != "n":
                        try:
                            enable_other_input = input("Please type \'y\' or \'n\': ").lower()
                        except:
                            traceback.print_exc()

                    if enable_other_input == "y":
                        self._enable_other_version_units = True
                    elif enable_other_input == "n":
                        self._enable_other_version_units = False