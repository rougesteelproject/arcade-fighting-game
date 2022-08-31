from constants import LIMIT_NUMBER_OF_PLAYERS
from menus.menu_console import MenuConsole as Menu
from team import Team
from unit import Unit
import logging

class BattleCreator():
    def __init__(self, callback, money_limit) -> None:
        
        self._callback = callback

        self._database_controller = self._callback._database_controler

        self._use_initiative = False
        self._use_variance = False
        self._set_game_version()

        self._money_limit = money_limit

        self._search_bar_units_data = []

        self._teams = []

        while len(self._teams) < 2:
            self._add_team()

    def _set_game_version(self):
        
        game_version_prompt = """
        1
        2
        3"""

        game_version_menu = Menu("Select game version: ", game_version_prompt, number_of_options=3)
        game_version_selection = game_version_menu.get_selection()
        
        user_confirmed_change = False
        print("Changing game version will recalculate the value of units. You may have to sell units in order to start the battle.")
        if game_version_selection > self._game_version:
            user_confirmed_change = self._warn_player_outdated_units()
        else:
            print("Are you sure you want to switch game version?")
            user_choice = ""
            while user_choice != "y" and user_choice != "n":
                user_choice = input("Please type \'y\' or \'n\': ")
            if user_choice == 'y':
                user_confirmed_change = True

        if user_confirmed_change:
            for team in self._teams:
                team.change_game_version_recalculate_units(self._game_version, game_version_selection)
            self._game_version = game_version_selection

            print(f"Game version set to {self._game_version}.")

            self._toggle_use_initiative()
            self._toggle_use_variance()

    def _reset_variance_and_initiative(self):
        if self._game_version == 1:
            print("Initiative turned off. Units take their turns at the same time.")
            self._use_initiative = False
            print("Variability turned off. Units always roll max for attacks and initiative.")
            self._use_variance = False

        elif self._game_version >= 2:
            print("Initiative turned on. Units will roll initiative.")
            self._use_initiative = True
            if self._game_version >= 3:
                print("Variability turned on. Units roll for initiative and damage.")
                self._use_variance = True

    def _toggle_use_initiative(self):
        if self._game_version >= 2:
            if self._use_initiative:
                print("Initiative turned off. Units take their turns at the same time.")
                self._use_initiative = False
            else:
                print("Initiative turned on. Units will roll initiative.")
                self._use_initiative = True

    def _toggle_use_variance(self):
        if self._game_version >= 3:
            if self._use_variance:
                print("Variability turned off. Units always roll max for attacks and initiative.")
                self._use_variance = False
            else:
                print("Variability turned on. Units roll for initiative and damage.")
                self._use_variance = True

    def _warn_player_outdated_units(self, game_version_selection):

        print("Moving from a lower game version to a higher one will sell units from earlier versions.")
        
        print("The following units will be refunded:")

        for team in self._teams:
            outdated_list = team.list_outdated_members(game_version_selection)

            if outdated_list != "":
                print('---')
                print(f'{team.name}:')
                print(outdated_list)

        print("Are you sure you want to switch game version?")
        user_choice = ""
        while user_choice != "y" and user_choice != "n":
            user_choice = input("Please type \'y\' or \'n\': ")
        if user_choice == 'y':
            user_confirmed_change = True

            for team in self._teams:
                team.sell_outdated_units(self._game_version, game_version_selection)

        return user_confirmed_change

    def _search_and_buy_units_by_name(self, name):
        self._search_bar_units_data = self._database_controller.get_unit_list_by_name(unit_name=name, game_version=self._game_version)

        unit_prompt = ""
        
        if len(self._search_bar_units_data) != 0:
            for index, unit_data in enumerate(self._search_bar_units_data):

                unit_power = unit_data[f'raw_power_v{self._game_version}']
                #diferent power for diferent game versions

                unit_prompt += f'{index}: {unit_data["name"]}: {unit_power} \n'


            unit_menu = Menu("Search Results:", unit_prompt, number_of_options=len(self._search_bar_units_data))

            unit_data = self._search_bar_units_data[unit_menu.get_selection()]
            

            team_prompt = ""

            for index, team in enumerate(self._teams):
                team_prompt += f'{index}: {team.name} \n'

            team_menu = Menu("Add to which team?", team_prompt, len(self._teams))

            team_selection = self._teams[team_menu.get_selection()]

            try:
                unit_selection = Unit(name=unit_data['name'], base_health=unit_data['base_health'], min_attack=unit_data['min_attack'], max_attack=unit_data['max_attack'], min_initiative=unit_data['min_initiative'], max_initiative=unit_data['max_initiative'], ai_type=unit_data['ai_type'], raw_power_v1=unit_data['raw_power_v1'], raw_power_v2=unit_data['raw_power_v2'], raw_power_v3=unit_data['raw_power_v3'], game_version=unit_data['game_version'], attack_verb=unit_data['attack_verb'])
                unit_selection._check_stat_validity()


                team_selection.buy(unit_selection, self._game_version)
            except:
                logging.exception()

    def _sell_unit(self):
        sell_team_prompt = """Select team to sell from: \n"""

        for index, team in enumerate(self._teams):
            sell_team_prompt += f'{index}: {team.name} \n'


        sell_team_menu = Menu("Sell: ", sell_team_prompt, len(self._teams))

        team_to_sell_from = self._teams[sell_team_menu.get_selection()]

        sell_unit_prompt = """"""

        for index, unit in enumerate(team_to_sell_from.members):
            sell_unit_prompt += f'{index}: {unit.name}: {unit.get_raw_power()} \n'

        sell_unit_menu = Menu("Which unit?", sell_unit_prompt, len(team_to_sell_from.members))

        team_to_sell_from.sell(team_to_sell_from.members[sell_unit_menu.get_selection()], self._game_version)

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
        self._callback.run_battle(self._teams, self._use_initiative, self._use_variance)

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
            6: [Empty Option]
            7: Toggle Variance
            8: Toggle Initiative
            """

            menu = Menu("Battle Creator", prompt, number_of_options=9)

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
                pass

            elif selection == 7:
                self._toggle_use_initiative()

            elif selection == 8:
                self._toggle_use_variance()