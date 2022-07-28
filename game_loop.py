import imp
from battle_creator import BattleCreator
from unit_creator import UnitCreator
from battle_coordinator import BattleCoordinator
from db_controllers.db_controler_sql import DatabaseControllerSQL
from db_controllers.dummy_db_controler import DummyDB
from menu import Menu
import traceback

class GameLoop():
    def __init__(self, db_type = "dummy") -> None:
        if db_type == "dummy":
            self._database_controler = DummyDB()
        elif db_type == "sql":
            self._database_controler = DatabaseControllerSQL()

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
                self._unit_creator = UnitCreator(self._database_controler)
                self._unit_creator.save_unit_to_db(self._unit_creator.get_input_unit_stats())

            elif selection == 1:
                try:
                    money_limit = int(input("What is the money limit for this battle? "))
                    self._battle_creator = BattleCreator(callback = self, money_limit=money_limit)
                    self._create_battle()
                except:
                    traceback.print_exc()
            
            elif selection == 2:
                exit = True        

    def _create_battle(self):
        self._battle_creator.loop()

    def run_battle(self, teams):
        self._battle_coordinator = BattleCoordinator(teams)
        self._battle_coordinator.run_battle()

gameloop = GameLoop(db_type="dummy")
gameloop.run()
