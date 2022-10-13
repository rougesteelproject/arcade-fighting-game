from arcade_view_classes.victory_screen import VictoryScreen
from battle_coordinator import BattleCoordinator
import constants
import arcade

from arcade_view_classes.sign_in_menu import SignInMenu
from arcade_view_classes.main_menu import MainMenu
from arcade_view_classes.battle_creator_menu import BattleCreatorMenu

class ArcadeUIHandler():

    def __init__(self, game_loop):

        self._game_loop = game_loop

        self._window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.GAME_NAME)

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

    def run(self):
        arcade.run()
    
    def create_sign_in_menu(self, error):
        self._sign_in_menu = SignInMenu(self._window, self._game_loop, error)
        self._window.show_view(self._sign_in_menu)

    def create_main_menu(self):
        self._main_menu = MainMenu(self._window, self._game_loop)
        self._window.show_view(self._main_menu)
    
    #TODO battle creator menu
    def create_battle_creator_menu(self):
        self._battle_creator_menu = BattleCreatorMenu(self._window, self._game_loop)
        self._window.show_view(self._battle_creator_menu)

    def create_battle_coordinator(self, teams, use_initiative, use_variance):
        self._battle_coordinator = BattleCoordinator(self._window, teams, use_initiative, use_variance, self._game_loop)
        self._battle_coordinator.setup()
        self._window.show_view(self._battle_coordinator)

    def create_victory_screen(self, victor):
        self._victory_screen = VictoryScreen(self._window, self._game_loop, victor)
        self._window.show_view(self._victory_screen)

    def exit(self):
        arcade.close_window()
        arcade.exit()

    #TODO Unit creator menu