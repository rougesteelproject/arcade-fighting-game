from constants import LIMIT_NUMBER_OF_PLAYERS
from battle_coordinator import BattleCoordinator
from db_controler_sql import DatabaseControllerSQL
from menu import Menu
from team import Team
import traceback

class BattleCreator():
    def __init__(self, callback, money_limit) -> None:
        self._database_controller = DatabaseControllerSQL()

        self._callback = callback

        self._money_limit = money_limit

        self._search_bar_units = []

        self._teams = []

        self._add_team()
        self._add_team()

    def _search_and_buy_units_by_name(self, name):
        self._search_bar_units = self._database_controller.get_unit_list_by_name(unit_name=name)

        unit_prompt = ""

        for index, unit in enumerate(self._search_bar_units):
            unit_prompt = unit_prompt + f'{index}: {unit.name}: {unit.price} \n'

        unit_menu = Menu("Search Results:", unit_prompt, number_of_options=len(self._search_bar_units) + 1)

        unit_selection = self._search_bar_units[unit_menu.get_selection()]

        team_prompt = ""

        for index, team in enumerate(self._teams):
            team_prompt = team_prompt + f'{index}: {team.name}'

        team_menu = Menu("Add to which team?", team_prompt, len(self._teams) +1)

        team_selection = self._teams[team_menu.get_selection()]

        try:
            team_selection.buy(unit_selection)
        except:
            traceback.print_exc()

    def _sell_unit(self):
        sell_team_prompt = """Select team to sell from: \n"""

        for index, team in enumerate(self._teams):
            sell_team_prompt = sell_team_prompt + f'{index}: {team.name}'


        sell_team_menu = Menu("Sell: ", sell_team_prompt)

        team_to_sell_from = self._teams[sell_team_menu.get_selection()]

        sell_unit_prompt = """"""

        for index, unit in enumerate(team_to_sell_from.members):
            sell_unit_prompt = sell_unit_prompt + f'{index}: {unit.name}: {unit.price} \n'

        sell_unit_menu = Menu("Which unit?", sell_unit_prompt, len(team_to_sell_from.members) + 1)

        team_to_sell_from.sell(team_to_sell_from.members[sell_unit_menu.get_selection()])

    def _add_team(self):
        print("Adding team: \n")
        team_name = input("Team name: ")

        self._teams.append(Team(team_name, self._money_limit))

    def _run_battle(self):
        self._callback.run_battle(self._teams)

    def loop(self):

        loop = True

        while loop:

            prompt = """
            0: Add team
            1: Search for a unit to add
            2: Sell a unit:
            3: Play the Battle!
            4: Exit to Main Menu
            """

            menu = Menu("Battle Creator", prompt, number_of_options=5)

            selection = menu.get_selection()

            if selection == 0:
                self._add_team()
                loop = False

            elif selection == 1:
                name = input("Unit Name (Search): ")
                self._search_and_buy_units_by_name(name)

            elif selection == 2:
                self._sell_unit()

            elif selection == 3:
                self._run_battle()
                loop = False

            elif selection == 4:
                loop = False