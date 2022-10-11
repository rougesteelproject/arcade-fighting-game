import constants
from battle_creator import BattleCreator
from arcade_ui_handler import ArcadeUIHandler

from battle_coordinator import BattleCoordinator

from db_controllers.db_controler_firestore import FirebaseDB

from copy import deepcopy

from sign_in_handler import SignInHandler

from google.oauth2.credentials import Credentials

import logging

class GameLoop():
    def __init__(self) -> None:

        self._ui_handler = ArcadeUIHandler(self)

        self._sign_in_handler = SignInHandler()

        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename= constants.ERROR_LOG_URI, encoding='utf-8', level=logging.ERROR, filemode='w')

        self.run_sign_in_prompt()
        self._ui_handler.run()

    def sign_in(self, email, password):
        #Credit to Bob Thomas

        response = self._sign_in_handler.sign_in_email_pass(email, password)
        
        if 'error' in response:
            self.run_sign_in_prompt(error = response['error']['message'])
        else:
            self._user_email = email
            
            # Use google.oauth2.credentials and the response object to create the correct user credentials
            credentials = Credentials(response['idToken'], response['refreshToken'])

            self._database_controler = FirebaseDB(credentials)

            self.run_main_menu()

    def run_sign_in_prompt(self, error = None):
        self._ui_handler.create_sign_in_menu(error)

    def run_main_menu(self):
        self._ui_handler.create_main_menu()

    def run_unit_creator_menu(self):
        self._ui_handler.create_unit_creator_menu()

    def save_unit(self, unit):
        self._database_controler.save_unit(unit)

    def create_battle(self):
        self._ui_handler.create_battle_creator_menu()
        self._battle_creator = BattleCreator(callback = self)
        self._battle_creator.dependant_init()

    def battle_creator_get_game_version(self):
        return self._battle_creator._game_version

    def battle_creator_get_outdated_list(self, new_game_version):
        return self._battle_creator.get_outdated_list(new_game_version)

    def battle_creator_set_game_version(self, new_game_version, sell_outdated_units):
        self._battle_creator._set_game_version(new_game_version, sell_outdated_units)

    def battle_creator_switch_version_popup(self, outdated_list = ""):
        self._ui_handler.battle_creator_create_switch_version_popup(outdated_list)

    def battle_creator_disable_initiative(self, use_initiative):
        pass
        #TODO
        #self._ui_handler.battle_creator_disable_initiative(use_initiative)

    def battle_creator_disable_variance(self, use_variance):
        pass
        #TODO
        #self._ui_handler.battle_creator_disable_variance(use_variance)

    def battle_creator_add_team(self, team_name):
        self._battle_creator._add_team(team_name)

    def battle_creator_remove_team(self, team_index):
        self._battle_creator._remove_team(team_index)

    def battle_creator_add_team_ui(self):
        pass
        #TODO
        #self._ui_handler.battle_creator_add_team()

    def battle_creator_buy_unit(self, unit_index, team_name):
        unit = deepcopy(self._database_controler.unit_data_list[unit_index])
        #Make a copy of the unit so it's not the same as the one in the db_cont
        self._battle_creator.buy_unit(unit, team_name)

    def battle_creator_use_initiative(self, use_initiative):
        self._battle_creator.use_initiative = use_initiative
        self.battle_creator_disable_initiative(use_initiative)

    def battle_creator_use_variance(self, use_variance):
        self._battle_creator.use_variance = use_variance
        self.battle_creator_disable_variance(use_variance)

    def search_units_by_name(self, query, game_version):
        return self._database_controler.get_unit_list_by_name(query, game_version)

    def battle_creator_set_money_limit(self, limit):
        self._battle_creator._set_money_limit(limit)

    def battle_creator_get_team_updates(self):

        money_limit = self._battle_creator._money_limit

        fetched_teams = self._battle_creator._teams
        
        return money_limit, fetched_teams

    def battle_creator_sell_unit(self, team_index, unit_index):
        self._battle_creator._sell_unit(team_index, unit_index)

    def battle_creator_rename_team(self, new_name, team_index):
        self._battle_creator.rename_team(new_name, team_index)

    def battle_creator_run_battle(self):
        self._battle_creator._run_battle()

    def run_battle(self):
        self._battle_coordinator = BattleCoordinator(self._battle_creator._teams, self._battle_creator.use_initiative, self._battle_creator.use_variance)
        self._battle_coordinator.run_battle()

        #TODO get rid of these two
        #self._ui_handler.clear_screen()
        #self._ui_handler.top_level.destroy()

gameloop = GameLoop()