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

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below

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

    #TODO the actual battle displayer

    #TODO Unit creator menu
