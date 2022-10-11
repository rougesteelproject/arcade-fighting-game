import arcade
import arcade.gui

import constants

class MainMenu(arcade.View):
    def __init__(self, window: arcade.Window = None, game_loop = None):
            super().__init__(window)

            self._game_loop = game_loop

            self._ui_manager = arcade.gui.UIManager()
            self._ui_manager.enable()

            self.v_box = arcade.gui.UIBoxLayout(space_between=5)

            self._create_battle_button = arcade.gui.UIFlatButton(text="Battle!", width=constants.MAIN_MENU_BUTTON_WIDTH)

            self._create_battle_button.on_click = self._create_battle

            self.v_box.add(self._create_battle_button)

            self._create_unit_button = arcade.gui.UIFlatButton(text= "Create Units [Disabled]", width=constants.MAIN_MENU_BUTTON_WIDTH)

            self._create_unit_button.on_click = self._create_unit

            self.v_box.add(self._create_unit_button)

            self._exit_button = arcade.gui.UIFlatButton(text="Exit", width=constants.MAIN_MENU_BUTTON_WIDTH)

            self._exit_button.on_click = self._exit_game

            self.v_box.add(self._exit_button)

            self._ui_manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.v_box)
            )

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.WHITE)

        # Create a box group to align the 'open' button in the center
        

    def on_hide_view(self):
        self._ui_manager.disable()
        return super().on_hide_view()

    def on_draw(self):
        """ Draw the menu """
        self.clear()

        self._ui_manager.draw()

    def _create_battle(self, event):
        self._game_loop.create_battle()

    def _create_unit(self, event):
        pass
        #TODO adjust gameloop?
        self._game_loop.create_unit()

    def _exit_game(self, event):
        pass
        #TODO create game_loop.exit
        self._game_loop.exit()