import constants
from battle_creator import BattleCreator
from unit_creator import UnitCreator
from battle_coordinator import BattleCoordinator
from db_controllers.db_controler_json import JSONDB
from menus.menu_console import MenuConsole as Menu
import logging



class GameLoop():
    def __init__(self) -> None:
        self._database_controler = JSONDB()

        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename= constants.ERROR_LOG_URI, encoding='utf-8', level=logging.ERROR, filemode='w')

    def run(self):
        exit = False

        while not exit:
            menu_name = """
            TIPS
            TEXT-BASED INACCURATE PLAGARISM SIMULATOR

            Main Menu:
            """

            prompt = """
            0: Create Units
            1: Battle!
            2: Exit
            """
            main_menu = Menu(menu_name, prompt, 3)

            selection = main_menu.get_selection()

            if selection == 0:
                try:
                    game_version = float(input("What version of the game is this unit for?"))

                    self._unit_creator = UnitCreator(self._database_controler)
                    self._unit_creator.save_unit_to_db(self._unit_creator.get_input_unit_stats(game_version))
                except:
                    logging.exception()

                

            elif selection == 1:
                try:
                    money_limit = int(input("What is the money limit for this battle? "))
                    self._battle_creator = BattleCreator(callback = self, money_limit=money_limit)
                    self._create_battle()
                except:
                    logging.exception()
            
            elif selection == 2:
                exit = True        

    def _create_battle(self):
        self._battle_creator.loop()

    def run_battle(self, teams, use_initiative, use_variance):
        self._battle_coordinator = BattleCoordinator(teams, use_initiative, use_variance=use_variance)
        self._battle_coordinator.run_battle()

gameloop = GameLoop()
gameloop.run()
